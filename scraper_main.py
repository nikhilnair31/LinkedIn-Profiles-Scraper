import os
import csv
import pandas as pd
from time import sleep
from parsel import Selector
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

load_dotenv()

CHROME_LOCAL_EXECUTABLE_PATH = str(os.getenv('CHROME_LOCAL_EXECUTABLE_PATH'))
CHROME_EXECUTABLE_PATH = str(os.getenv('CHROME_EXECUTABLE_PATH'))
BINARY_LOCATION = str(os.getenv('BINARY_LOCATION'))
SEARCH_QUERY = str(os.getenv('SEARCH_QUERY'))
FILE_NAME = str(os.getenv('FILE_NAME'))
LINKEDIN_USERNAME = str(os.getenv('LINKEDIN_USERNAME'))
LINKEDIN_PASSWORD = str(os.getenv('LINKEDIN_PASSWORD'))

# function to ensure all key data fields have a value
def validate_field(field):
    if field is None:
        field = 'No results'
    return field

driver = webdriver.Chrome('chromedriver')
driver.get('https://www.linkedin.com')

username = driver.find_element(By.ID, 'session_key')
username.send_keys(LINKEDIN_USERNAME)
sleep(0.5)

password = driver.find_element(By.ID, 'session_password')
password.send_keys(LINKEDIN_PASSWORD)
sleep(0.5)

sign_in_button = driver.find_element(By.XPATH, '//*[@type="submit"]')
sign_in_button.click()
sleep(50)

driver.get('https:www.google.com')
sleep(3)

search_query = driver.find_element(By.NAME, 'q')
search_query.send_keys(SEARCH_QUERY)
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(3)

search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")
linkedin_urls = []
for result in search_results:
    link = result.find_element(By.TAG_NAME, "a")
    href = link.get_attribute("href")
    if href.startswith("http"):
        linkedin_urls.append(href)

# linkedin_urls = driver.find_elements(By.CSS_SELECTOR, ".iUh30")
# linkedin_urls = [url.text for url in linkedin_urls]
print(f'linkedin_urls - {len(linkedin_urls)}\n')
for url in linkedin_urls:
    print(f'{url}')
sleep(0.5)

datalist = [['Name', 'Job Title', 'Company', 'College', 'Location', 'URL']]

# For loop to iterate over each URL in the list
for linkedin_url in linkedin_urls:
    driver.get(linkedin_url)
    sleep(5)
    sel = Selector(text=driver.page_source) 

    name = ''
    job_title = ''
    company = ''
    college = ''
    location = ''

    linkedin_url = driver.current_url
    name_section_element = driver.find_element_by_xpath('//section[@id="ember365", "Experience")]')
    name_element = name_section_element.find_element(By.XPATH, '//h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]').text
    if name_element:
        name = name_element.strip()
    job_title_section_element = driver.find_element_by_xpath('//section[@id="ember371", "Education")]')
    job_title_element = driver.find_element(By.XPATH, '//div[@class="display-flex flex-wrap align-items-center full-height"]/span[contains(@class, "t-bold")]/text()').text
    if job_title_element:
        job_title = job_title_element.strip()
    # company_element = driver.find_element(By.XPATH, '//div[contains(@class, "pvs-entity")]/div/a/@href').text
    # if company_element:
    #     company = company_element.strip()
    # education_section_element = driver.find_element_by_xpath('//h2[contains(text(), "Education")]')
    # college_element = education_section_element.find_element_by_xpath('..//li[@class="artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"]//span[contains(@class, "t-bold")]').text
    # if college_element:
    #     college = college_element.strip()
    # location_element = driver.find_element(By.XPATH, '//span[contains(@class, "t-black--light") and contains(@class, "ellipsis")]/text()').text
    # if location_element:
    #     location = location_element.strip()

    # validating if the fields exist on the profile
    name = validate_field(name)
    job_title = validate_field(job_title)
    # company = validate_field(company)
    # college = validate_field(college)
    # location = validate_field(location)
    # linkedin_url = validate_field(linkedin_url)
    
    curr = [name, job_title]#, company, college, location, linkedin_url]
    datalist.append(curr)
    print(f'\n{curr}\n')

df = pd.DataFrame(datalist[1:], columns=datalist[0])
df.to_csv(FILE_NAME, index=False)

# terminates the application
driver.quit()