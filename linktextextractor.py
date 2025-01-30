import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def fetch_article_text(url):
    """
    Extracts the main text content from a news article while handling cookies using requests.Session().

    :param url: The article URL.
    :return: Extracted article text or error message.
    """
    try:
        # Create a persistent session (stores cookies automatically)
        session = requests.Session()

        # Define headers to mimic a real browser
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0_0) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/130.0.6723.70 Safari/537.36"
            ),
            "Referer": "https://www.google.com/",  # Helps bypass some bot detections
        }

        # First request (loads cookies)
        response = session.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()  # Raise error for 4xx/5xx responses

        # Second request (uses stored cookies)
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse the webpage using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text from paragraph tags <p> only
        paragraphs = soup.find_all('p')
        article_text = "\n".join(p.get_text() for p in paragraphs if p.get_text())

        # If no text is found, return an error message
        return article_text.strip() if article_text else "No readable text found"

    except requests.exceptions.RequestException as e:
        # Return error message for failed requests (e.g., timeouts, 404 errors)
        return f"Error: {e}"

def process_csv(input_csv, output_csv, error_log_csv):
    """
    Reads a CSV file with news article links, extracts text from each link,
    and writes the data into a new CSV file with an additional "Article Text" column.
    Also logs any failed extractions in a separate error CSV.

    :param input_csv: The name of the input CSV file (from the first script).
    :param output_csv: The name of the output CSV file with extracted text.
    :param error_log_csv: The name of the CSV file where errors will be logged.
    """
    # Read the input CSV file using pandas
    df = pd.read_csv(input_csv)

    # Ensure the required columns exist
    if not {"Title", "Source URL", "Source Name"}.issubset(df.columns):
        print("Error: Required columns not found in the CSV file.")
        return

    # Add a new column for the extracted article text
    df["Article Text"] = ""

    # Create a list to store failed extractions
    failed_extractions = []

    # Loop through each row in the dataframe
    for index, row in df.iterrows():
        url = row["Source URL"]

        # Skip empty URLs
        if pd.isna(url) or url.strip() == "":
            print(f"Skipping empty URL at row {index + 1}")
            failed_extractions.append({"Source URL": "EMPTY", "Error": "No URL provided"})
            continue

        print(f"Extracting text from: {url} ({index+1}/{len(df)})")

        # Extract the article text from the given URL
        article_text = fetch_article_text(url)

        # If extraction failed, add it to the error log
        if article_text.startswith("Error"):
            failed_extractions.append({"Source URL": url, "Error": article_text})
        else:
            # Otherwise, save the extracted text to the dataframe
            df.at[index, "Article Text"] = article_text

        # Pause between requests to avoid overloading the website (optional)
        time.sleep(1)

    # Save the successfully extracted data to a new CSV file
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"Finished processing. New file saved as: {output_csv}")

    # Save failed extractions to a separate CSV file
    if failed_extractions:
        error_df = pd.DataFrame(failed_extractions)
        error_df.to_csv(error_log_csv, index=False, encoding="utf-8")
        print(f"Failed extractions logged in: {error_log_csv}")

def main():
    """
    Main function to process the CSV file and extract article text.
    """
    input_csv = "news_results.csv"     # Input file (from the previous script)
    output_csv = "news_with_text.csv"  # Output file with extracted article text
    error_log_csv = "failed_extractions.csv"  # Log file for failed extractions

    # Run the processing function
    process_csv(input_csv, output_csv, error_log_csv)

if __name__ == "__main__":
    main()
