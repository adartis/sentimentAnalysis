import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ---- configure selenium ----
chrome_options = Options()
#  chrome_options.add_argument("--headless=new")  run without visible window
driver = webdriver.Chrome(options=chrome_options)

# ---- read input csv ----
df = pd.read_csv("news_results.csv")

# ---- prepare new column ----
actual_urls = []

for i, link in enumerate(df["url"], 1):
    try:
        driver.get(link)

        # small pause to let redirects happen
        time.sleep(4)

        # capture resolved url
        resolved = driver.current_url
    except Exception as e:
        resolved = f"ERROR: {e}"

    actual_urls.append(resolved)
    print(f"{i}/{len(df)}: {link} -> {resolved}")

# ---- add to dataframe ----
df["actual_url"] = actual_urls

# ---- save result ----
df.to_csv("output.csv", index=False)

driver.quit()
