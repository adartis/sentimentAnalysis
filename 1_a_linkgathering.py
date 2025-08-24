# 'csv' is used to write data to a CSV file.
import csv
# 'requests' is used to make HTTP requests.
import requests
# 'feedparser' helps parse RSS feed content.
import feedparser
# 'urllib.parse' is used to process and extract information from URLs, removing previous regex usage
#import re
from urllib.parse import urlparse, parse_qs
# 'datetime' is used to work with dates.
from datetime import datetime
# 'logging' provides a way to output messages (instead of using print statements).
import logging

# Configure the logging module.
# This setup will display informational and error messages in the console.
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def extract_real_url(google_news_url: str) -> str:
    """
    Extracts the actual article URL from a Google News redirect link.
    
    Some Google News RSS feed entries do not directly link to the article, but rather to
    a redirect URL. This function checks if there is a query parameter named 'url' in the
    link. If found, it returns the value of this parameter which is the actual URL.
    
    Parameters:
    google_news_url (str): The URL obtained from the Google News RSS entry.
    
    Returns:
    str: The direct article URL if available, otherwise the original URL.
    """
    # Use 'urlparse' to break the URL into its components.
    parsed = urlparse(google_news_url)
    # 'parse_qs' extracts the query parameters from the URL into a dictionary.
    query_params = parse_qs(parsed.query)
    # If the query parameters contain 'url', use it as the real URL.
    if "url" in query_params:
        return query_params["url"][0]  # Return the first value for the 'url' parameter.
    # If no 'url' parameter exists, return the original URL.
    return google_news_url

def scrape_google_news_rss(search_terms, csv_filename, start_date, end_date):
    """
    Scrapes the Google News RSS feed for articles matching the search terms.
    It filters the articles based on a given date range and writes the results to a CSV file.
    
    Parameters:
    search_terms (str): The query used to search news articles.
    csv_filename (str): The name of the CSV file where the results will be saved.
    start_date (datetime): The start date for filtering articles.
    end_date (datetime): The end date for filtering articles.
    """

    # Replace spaces in the search query with '+' so that the URL is properly formatted.
    encoded_search = search_terms.replace(" ", "+")

    # Construct the RSS feed URL using the encoded search terms.
    # The parameters 'hl', 'gl' and 'ceid' ensure the results are in English and for a specific region.
    rss_url = f"https://news.google.com/rss/search?q={encoded_search}&hl=en-US&gl=US&ceid=US:en"

    # Define HTTP headers, including a User-Agent string.
    # This helps to mimic a standard web browser and may prevent the request from being blocked.
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0_0) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/130.0.6723.70 Safari/537.36"
        )
    }

    try:
        # Make an HTTP GET request to the RSS URL.
        response = requests.get(rss_url, headers=headers, timeout=10)
        # If the request returns an error status (such as 404 or 500), raise an exception.
        response.raise_for_status()

        # Parse the RSS feed content using 'feedparser'.
        feed = feedparser.parse(response.text)
        # Log the number of articles found in the feed.
        logger.info(f"Number of articles found: {len(feed.entries)}")

        # Print number of articles found (useful for debugging)
        print(f"Number of articles found: {len(feed.entries)}")

       # If no articles were found, log a message and exit the function.
        if not feed.entries:
            logger.info("No articles found. Please check the search query or the RSS feed URL.")
            return

        # Open the specified CSV file in write mode.
        # 'encoding' is set to 'utf-8' to support various characters and 'newline' prevents blank lines.
        with open(csv_filename, mode='w', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Write the header row to the CSV file.
            writer.writerow(["title", "url", "source_name", "date_found"])
            

            # Iterate over each entry (article) in the RSS feed.
            for entry in feed.entries:
                # Extract the article title. If no title is found, use an empty string.
                title = entry.get("title", "").strip()
                # Extract the URL provided by Google News for the article.
                google_news_url = entry.get("link", "").strip()
                # Retrieve the news source's name if available.
                # The attribute 'source' should contain a 'title' that gives the source name.
                source_name = entry.source.title if hasattr(entry, "source") else "Unknown"
                # Use the helper function to obtain the actual URL of the article.
                source_url = extract_real_url(google_news_url)

                # Check if the article has a published date.
                if hasattr(entry, "published_parsed"):
                    # Convert the published date to a datetime object.
                    article_date = datetime(*entry.published_parsed[:6])
                else:
                    article_date = None  # If no date is available, set it to None.

                # Only include articles that have a valid date or fall within the specified date range.
                if article_date or start_date <= article_date <= end_date:
                    # Format the date as "YYYY-MM-DD" and write the article details to the CSV file.
                    writer.writerow([title, source_url, source_name, article_date.strftime("%Y-%m-%d")])

        # Log a confirmation message that the CSV file has been created.
        logger.info(f"CSV file '{csv_filename}' has been created successfully.")

    except requests.exceptions.RequestException as e:
        # Log an error message if the HTTP request fails.
        logger.error(f"Error fetching RSS feed: {e}")

def main() -> None:
    """
    The main function sets the parameters for the search and the date range.
    It then calls the scraping function to process the Google News RSS feed.
    """
    # Define the search terms for the news query.
    search_terms = "Serbia Government SNS EU when:100d"
    # Specify the output CSV file name.
    csv_filename = "news_results.csv"
    # Set the start date for the articles (in year, month, day format).
    start_date = datetime(2025, 1, 25)
    # Set the end date for the articles.
    end_date = datetime(2025, 2, 4)
    
    # Call the function to scrape the RSS feed and write the results to the CSV file.
    scrape_google_news_rss(search_terms, csv_filename, start_date, end_date)

# This conditional ensures that the 'main' function runs only if this script is executed directly.
if __name__ == "__main__":
    main()