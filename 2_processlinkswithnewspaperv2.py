# import pandas for dataframe manipulation
import pandas as pd
# import time for moderating speed of requests
import time
# import newspaper for text extraction
from newspaper import Article
# import logging for logging details
import logging

# Configure logging to show information messages.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# File paths
INPUT_CSV = "news_results.csv"   # Input CSV file with URLs - built
OUTPUT_CSV = "news_results_with_text.csv"  # Output CSV file - currently empty

# Read the CSV (assuming it has one column named "Links")
df = pd.read_csv(INPUT_CSV)

def extract_article_text(url: str) -> str:
    """
    Extracts the article text from the given URL using the Newspaper module.
    
    Limits the text to 5000 characters.
    If an error occurs, returns an error message.
    
    Parameters:
    url (str): The URL of the article.
    
    Returns:
    str: The extracted text or an error message.
    """
    try:
        # defines article variable by URL, downloads and parses with newspaper limiting to 5000 characters
        article = Article(url)
        article.download()
        article.parse()
        return article.text[:5000]
        # exception if error processing URL
    except Exception as e:
        logger.error(f"Error processing URL {url}: {e}")
        return f"Failed to extract: {str(e)}"
    
# main function to encapsulate dataframe manupulation
def main() -> None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(INPUT_CSV)
    
    # Check that the required columns exist.
    required_columns = {"title", "url", "source_name", "date_found", "actual_url"}
    # test for columns
    if not required_columns.issubset(df.columns):
        logger.error(f"Input CSV must contain the columns: {required_columns}")
        return

    # Add a new column 'text' to the DataFrame.
    # Initially, this column can be empty.
    df["text"] = ""
    
    # Loop through each row in the DataFrame.
    for index, row in df.iterrows():
        url = row["actual_url"]
        # logging for testing
        logger.info(f"Processing {index+1}/{len(df)}: {url}")
        # Extract the article text from the URL.
        article_text = extract_article_text(url)
        # Update the 'text' column for this row.
        df.at[index, "text"] = article_text
        # Pause briefly to avoid overloading the server - two seconds
        time.sleep(2)
    
    # Write the updated DataFrame to a new CSV file.
    # The output CSV will contain the original headers plus the new 'text' column.
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    logger.info(f"Extraction complete! Data saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()