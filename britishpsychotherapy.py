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
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36")
driver = webdriver.Chrome('chromedriver', options=chrome_options)
MAIN_URL = 'https://www.britishpsychotherapyfoundation.org.uk/find-a-therapist?display_name=&city=&language_25=All&gender=All&state_province=All&accessibility_32=All&therapy_type_26=All&region_1=All&remote_therapy_capability_87=All&geo_code_1=&postcode_from=&from_miles=&page='
date = datetime.now().strftime("%Y%m%d-%H%M%S")
CSV_FILE = f'britishpsychotherapy_output_{date}'


# counsellors, psychotherapists, clinical psychologists

def get_information(url):
    driver.get(url)

    contenido = driver.find_elements(By.XPATH, '//tbody//tr')

    # Nombre y Email
    for item in contenido:
        try:
            name = item.find_elements(By.CLASS_NAME, 'views-field-display-name')[0].text
            contenedor = item.find_elements(By.CLASS_NAME, 'views-field-nothing-2')[0]
            link_element = contenedor.find_elements(By.TAG_NAME, 'a')[0]
            email = link_element.get_attribute('href')
            email = email.split('mailto:')[1]

            data = {
                'email': email,
                'name': name,
                'url': url
            }

            json_db(data=data)

           # make_csv(name, email, url)

        except Exception as e:
            # print(e)
            pass


def next_page(url):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[text() = "next ›"]')))
        next_xpath = driver.find_elements(By.XPATH, '//*[text() = "next ›"]')
        return True
    except:
        return False


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
    count = 0

    while (True):
        next = next_page(MAIN_URL + str(count))
        print("===========[PAGE]======================")
        print(f'Pagina: {count}')
        print("===========[PAGE]======================")
        if next == True:
            #print("===========[PROFILES]======================")
            count = count + 1
            info = get_information(MAIN_URL + str(count))
            #print("===========[PROFILES]======================")
        else:
            print("============[FINISH]=====================")
            print(MAIN_URL + str(count))
            print('Termino')
            print("=============[FINISH]====================")
            break

driver.get_screenshot_as_file('Page.png')
driver.quit()
