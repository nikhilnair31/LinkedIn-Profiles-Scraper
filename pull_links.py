# region Packages
import os
import csv
import pandas as pd
from time import sleep
from parsel import Selector
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# endregion

# region Setup
load_dotenv()

CHROME_LOCAL_EXECUTABLE_PATH = str(os.getenv('CHROME_LOCAL_EXECUTABLE_PATH'))
CHROME_EXECUTABLE_PATH = str(os.getenv('CHROME_EXECUTABLE_PATH'))
BINARY_LOCATION = str(os.getenv('BINARY_LOCATION'))
SEARCH_QUERY = str(os.getenv('SEARCH_QUERY'))
FILE_NAME = str(os.getenv('FILE_NAME'))
LINKEDIN_USERNAME = str(os.getenv('LINKEDIN_USERNAME'))
LINKEDIN_PASSWORD = str(os.getenv('LINKEDIN_PASSWORD'))
# endregion

# region Functions
def append_url():
    search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")
    for result in search_results:
        link = result.find_element(By.TAG_NAME, "a")
        href = link.get_attribute("href")
        if href.startswith("http"):
            linkedin_urls.append(href)
# endregion

# region Main
driver = webdriver.Chrome('chromedriver')
driver.get('https:www.google.com')
sleep(3)

search_query = driver.find_element(By.NAME, 'q')
search_query.send_keys(SEARCH_QUERY)
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(3)

# region Scrapingg
linkedin_urls = []
# 1st page scraped
append_url()
# 2nd page onwards scraped
for i in range(2, 10):
    next_button = driver.find_element(By.XPATH, '//a[@id="pnnext"]')
    next_button.click()
    sleep(2)
    append_url()
# endregion

# region Print
print(f'linkedin_urls - {len(linkedin_urls)}\n')
for url in linkedin_urls:
    print(f'{url}')
sleep(0.5)
# endregion

# region Saving
df = pd.DataFrame({'URL': linkedin_urls})
df.to_csv(FILE_NAME, index=False, header=['URL'])
# endregion

driver.quit()
# endregion