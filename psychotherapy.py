from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
import csv
import os.path
from datetime import datetime

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36")
driver = webdriver.Chrome('chromedriver', options=chrome_options)
MAIN_URL = 'https://www.psychotherapy.org.uk/find-a-therapist/?Distance=30&page='
date = datetime.now().strftime("%Y%m%d-%H%M%S")
CSV_FILE = f'output_{date}'

def get_profile(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="light-anchor"]')))
    profile_xpath = driver.find_elements(By.XPATH, '//*[@class="light-anchor"]')
    profile_link = []
    for item in profile_xpath:
        profile_link.append(item.get_attribute("href"))
    return profile_link


def get_information(url):
    driver.get(url)
    try:
        email_xpath = driver.find_elements(By.XPATH, '//*[text() = "Email Therapist"]')
        email_link = email_xpath[0].get_attribute("href")
        email = email_link.split('mailto:')[1]

        name_xpath = driver.find_elements(By.XPATH, '//h1')
        name = name_xpath[0].text

        json = {
            'name': name,
            'email': email,
            'url': url
        }

        return json
    except:
        pass

def next_page(url):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="js-page-number-trigger page-link page-link-next"]')))
        next_xpath = driver.find_elements(By.XPATH, '//*[@class="js-page-number-trigger page-link page-link-next"]')
        return True
    except:
        return False

def make_csv(name,email,url):
    file_exits = os.path.isfile(f'{CSV_FILE}.csv')
    csvFile = open(f'{CSV_FILE}.csv', 'a')
    try:
        headers = ['Name', 'Email', 'Url']
        #writer = csv.writer(csvFile)
        writer = csv.DictWriter(csvFile, delimiter=',', lineterminator='\n', fieldnames=headers)
        if not file_exits:
            writer.writeheader()
        name = name.encode('utf-8')
        writer.writerow({'Name': name,'Email': email,'Url': url})
    finally:
        csvFile.close()

if __name__ == '__main__':
    count = 1

    while(True):
        next = next_page(MAIN_URL + str(count))
        print("===========[PAGE]======================")
        print(MAIN_URL + str(count))
        print("===========[PAGE]======================")
        if next == True:
            profiles = []
            count = count + 1
            profiles.append(get_profile(MAIN_URL + str(count)))
            print("===========[PROFILES]======================")
            for item in profiles:
                for profile in item:
                    print(profile)
                    info = get_information(profile)
                    if info != None:
                        # person_information.append(info)
                        name = info['name']
                        email = info['email']
                        url = info['url']
                        make_csv(name, email, url)
            print("===========[PROFILES]======================")
        else:
            print("============[FINISH]=====================")
            print(MAIN_URL + str(count))
            print('Termino')
            print("=============[FINISH]====================")
            break

    driver.get_screenshot_as_file('Page.png')
    driver.quit()
    #print(person_information)