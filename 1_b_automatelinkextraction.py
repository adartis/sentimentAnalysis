import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Path to your ChromeDriver
driver_path = 'path/to/chromedriver'

# Start the WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Read the CSV file
df = pd.read_csv('news_results.csv')

# Function to get the actual link from the redirect
def get_actual_link(redirect_url):
    driver.get(redirect_url)
    time.sleep(3)  # Allow redirection
    return driver.current_url

# List to store extracted links
extracted_links = []

# Iterate through each URL in the CSV
for url in df['url']:
    try:
        original_url = get_actual_link(url)
        extracted_links.append(original_url)
    except Exception as e:
        extracted_links.append(None)  # Add None if failed
        print(f"Failed to get link for {url}: {e}")

# Add the extracted links as a new column
df['links'] = extracted_links

# Save the new CSV file
df.to_csv('news_results_with_links.csv', index=False)

# Close the driver
driver.quit()

print("Links have been extracted and saved to 'news_results_with_links.csv'.")
