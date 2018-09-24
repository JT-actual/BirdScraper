import csv
import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException


# Start script timer
start = time.time()

# Set Firefox driver options for running headless
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

# Telling script to keep trying action for 20 seconds before returning error
driver.implicitly_wait(20)

# Initialize Firefox driver
driver.get("https://ebird.org/media/catalog?mediaType=p&region=United%20States%20(US)&regionCode=US")

# Selecting "Best Quality" from dropdown menu & waiting for page to reload
driver.find_element_by_xpath('//*[@id="SearchToolbar-mainPanel"]/div[2]/div[3]/fieldset/a').click()
driver.find_element_by_xpath('//*[@id="RadioGroup-sort"]/span[2]/label/span').click()
time.sleep(10)

# AJAX button - Sends post request for 50x more pictures loaded to site
show_more_button = driver.find_element_by_xpath('//*[@id="show_more"]')

# While loop clicks 'show more' button until 'if count' statement criteria met - Also prints loop count
count = 1
while count > 0:
    try:
        time.sleep(.5)
        show_more_button.click()
    except ElementNotVisibleException:
        close_img_button = driver.find_element_by_xpath('/html/body/div[2]/button')
        close_img_button.click()
    except WebDriverException:
        show_more_button.click()
    except StaleElementReferenceException:
        show_more_button.click()
    count = count + 1
    print(count)
    if count == 20000:
        break

# End script timer and print value in seconds
end = time.time()
print(end - start)

# Hand off from Selenium to BeautifulSoup for HTML parsing
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Looping through HTML, extracting Alt-Text & Source URL data into dictionary
img_data = []
for img_tag in soup.find_all('img'):
    data_dict = dict()
    data_dict['image_name'] = img_tag['alt']
    data_dict['image_url'] = img_tag['src']
    img_data.append(data_dict)

# Writing scraped data to CSV file
with open('XYZtest.csv', 'w', newline='') as birddata:
    fieldnames = ['image_name', 'image_url']
    writer = csv.DictWriter(birddata, fieldnames=fieldnames)
    writer.writeheader()
    for data in img_data:
        writer.writerow(data)

# Killing the driver when finished
# change sleep to 1000 sec when in production
time.sleep(1000)
driver.close()
