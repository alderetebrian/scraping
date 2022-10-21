from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
import csv
import os.path
from datetime import datetime
from json_db import json_db

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36")
driver = webdriver.Chrome('chromedriver', options=chrome_options)
MAIN_URL = "https://www.hgi.org.uk/"
date = datetime.now().strftime("%Y%m%d-%H%M%S")
CSV_FILE = f'hgi_output_{date}'
page_number = 0


# counsellors, psychotherapists, clinical psychologists

def get_profile(url):
    #Unfortunately we couldn't find any therapists matching your search, please try again.
    lista_profiles = []
    driver.get(url)
    html = driver.page_source
    if "Unfortunately we couldn't find any therapists matching your search, please try again." in html:
        return 'no'
    profiles = driver.find_elements(By.XPATH, '//ul[@class="reset-list"]//li[@class="node-readmore first last"]/a')
    for profile in profiles:
        lista_profiles.append(profile.get_attribute('href'))
    return lista_profiles

def get_information(url):
    driver.get(url)
    contenido = driver.find_elements(By.XPATH, '//main[@id="content"]')[0]
    name = contenido.find_elements(By.XPATH, './/h1')
    email = contenido.find_elements(By.XPATH, '//span[@class="email-address"]//a[starts-with(@href,"mailto:")]')
    if not email:
        pass
    else:
        name = name[0].text
        email = email[0].text
        print(url)
        print(name)
        print(email)
        #make_csv(name, email, url)
        data = {
            'email': email,
            'name': name,
            'url': url
        }

        json_db(data=data)


def make_csv(name, email, url):
    file_exits = os.path.isfile(f'{CSV_FILE}.csv')
    csvFile = open(f'{CSV_FILE}.csv', 'a')
    try:
        headers = ['Name', 'Email', 'Url']
        # writer = csv.writer(csvFile)
        writer = csv.DictWriter(csvFile, delimiter=',', lineterminator='\n', fieldnames=headers)
        if not file_exits:
            writer.writeheader()
            #name = name.encode('utf-8')
        writer.writerow({'Name': name, 'Email': email, 'Url': url})
    finally:
        csvFile.close()


# ('//*[text() = "next ›"]')

if __name__ == '__main__':
    while True:
        PAGE_URL = f"/find-therapist/search?field_positions_latlon=&field_positions_latlon_op=-&title=&field_language_spoken=All&field_specialist_areas=All&page={page_number}"
        URL = MAIN_URL + PAGE_URL
        print(URL)
        profiles = get_profile(URL)
        if profiles == 'no':
            print('Finalizo el proceso')
            break
        for profile in profiles:
            get_information(profile)
        page_number = page_number + 1
    driver.quit()
