# This tool gathers article links from Google News RSS based on user-defined search terms
import csv
import requests
from bs4 import BeautifulSoup
import feedparser
import re

def scrape_google_news_rss(search_terms, csv_filename):
    """
    Scrapes Google News RSS for the specified search terms and saves results to a CSV file.

    :param search_terms: The search query (e.g., "Serbia Government").
    :param csv_filename: The name of the output CSV file (e.g., "news_results.csv").
    """
    
    # Replace spaces with '+' to format the search query for Google News RSS
    encoded_search = search_terms.replace(" ", "+")
    
    # Google News RSS URL with regional settings for English results
    rss_url = f"https://news.google.com/rss/search?q={encoded_search}&hl=en-US&gl=US&ceid=US:en"

    # Define a User-Agent to avoid being blocked by Google or news websites
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0_0) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/130.0.6723.70 Safari/537.36"
        )
    }

    try:
        # Send an HTTP GET request to Google News RSS
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors

        # Parse the RSS feed using feedparser
        feed = feedparser.parse(response.text)

        # Print number of articles found (useful for debugging)
        print(f"Number of articles found: {len(feed.entries)}")

        # If no articles are found, print a message and exit
        if not feed.entries:
            print("No articles found. Check the RSS URL or try a different search term.")
            return

        # Open the CSV file for writing (overwrite mode)
        with open(csv_filename, mode='w', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            
            # Write the CSV header row
            writer.writerow(["Title", "Source URL", "Source Name"])

            # Iterate through each news article entry in the RSS feed
            for entry in feed.entries:
                title = entry.get("title", "").strip()  # Extract the article title
                google_news_url = entry.get("link", "").strip()  # Extract Google News link
                source_name = entry.source.title if hasattr(entry, "source") else "Unknown"  # Extract source name
                
                # Extract the actual source URL from Google's redirect
                source_url = extract_real_url(google_news_url)

                # Write extracted data to the CSV file
                writer.writerow([title, source_url, source_name])
        
        print(f"CSV file '{csv_filename}' has been created successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS feed: {e}")

def extract_real_url(google_news_url):
    """
    Extracts the actual article URL from a Google News redirect link.

    :param google_news_url: The Google News RSS link.
    :return: The direct source URL.
    """
    # Google sometimes adds 'url=' in its redirects, but often it’s not present
    match = re.search(r'url=(https?://[^&]+)', google_news_url)
    
    if match:
        return match.group(1)  # Extract and return the real URL
    
    return google_news_url  # If no match, return the original link (it may be direct)

def main():
    """
    Main function to execute the scraping process.
    """
    search_terms = "Serbia protests"  # Define search terms (modify as needed)
    csv_filename = "news_results.csv"  # Define output CSV filename

    # Call the scraper function
    scrape_google_news_rss(search_terms, csv_filename)

if __name__ == "__main__":
    main()  # Run the main function
