from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
import csv
import os.path
from datetime import datetime
import re
from config import ini_read
from json_db import json_db

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36")
driver_path = ini_read()
driver = webdriver.Chrome(driver_path, options=chrome_options)
MAIN_URL = 'https://www.bacp.co.uk/search/Therapists?q=mind&skip='
date = datetime.now().strftime("%Y%m%d-%H%M%S")
CSV_FILE = f'bacp_output_{date}'

def get_profile(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[text() = "View profile"]')))
        profile_xpath = driver.find_elements(By.XPATH, '//*[text() = "View profile"]')
        profile_link = []
        for item in profile_xpath:
            profile_link.append(item.get_attribute("href"))
        return profile_link
    except:
        pass

def get_url(url):
    try:
        driver.get(url)
        web_page = driver.find_elements(By.XPATH, '//*[@class="directory-section__address content"]')[0]
        web_page = web_page.find_elements(By.TAG_NAME, 'a')[0]
        web_page = web_page.get_attribute("href")
        link = web_page
        name = driver.find_elements(By.CLASS_NAME, 'template-directory__name')[0].text

        json = {
            'name': name,
            'link': link
        }
        return json
    except:
        pass

def get_information(url):
    try:
        driver.get(url)
        email_regex = r'([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)'
        text = driver.find_elements(By.TAG_NAME, "body")[0].get_attribute("innerText")
        email = re.search(email_regex, text).group(0)
        return email
        #print(text)
        # email_xpath = driver.find_elements(By.XPATH, '//*[text() = "Email Therapist"]')
        # email_link = email_xpath[0].get_attribute("href")
        # email = email_link.split('mailto:')[1]
        #
        # name_xpath = driver.find_elements(By.XPATH, '//h1')
        # name = name_xpath[0].text
        #
        # json = {
        #     'name': name,
        #     'email': email,
        #     'url': url
        # }
        #
        # return json
    except:
        pass

def next_page(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[text() = "Next"]')))
        next_xpath = driver.find_elements(By.XPATH, '//*[text() = "Next"]')
        return True
    except:
        return False

def break_page(url):
    try:
        driver.get(url)
        break_xpath = driver.find_elements(By.XPATH, '//*[contains(text(),"Try searching for something else instead.")]')
        if break_xpath != []:
            return True
        else:
            return False
    except:
        return False

def make_csv(name,email,url):
    file_exits = os.path.isfile(f'{CSV_FILE}.csv')
    csvFile = open(f'{CSV_FILE}.csv', 'a')
    try:
        headers = ['Name', 'Email', 'Url']
        #writer = csv.writer(csvFile)
        #writer = csv.DictWriter(csvFile, delimiter=',', lineterminator='\n', fieldnames=headers)
        writer = csv.DictWriter(csvFile, delimiter=';', lineterminator='\n', fieldnames=headers)
        if not file_exits:
            writer.writeheader()
        #name = name.encode('utf-8')
        writer.writerow({'Name': name,'Email': email,'Url': url})
    finally:
        csvFile.close()

if __name__ == '__main__':
    #count = 0
    #count = 1950
    #count = 4840
    #count = 5180
    #count = 5570
    #count = 5630
    #count = 5660
    #count = 7440
    #count = 8240
    #count = 10880
    #count = 12340
    #count = 14350
    #count = 14480
    count = 0
    while(True):
        #next = next_page(MAIN_URL + str(count))
        break_web = break_page(MAIN_URL + str(count))
        print("===========[PAGE]======================")
        print(MAIN_URL + str(count))
        print("===========[PAGE]======================")
        #if next == True:
        if break_web == False:
            profiles = []
            count = count + 10
            profiles.append(get_profile(MAIN_URL + str(count)))
            print("===========[PROFILES]======================")
            for profile in profiles[0]:
                try:
                    info = get_url(profile)
                    name = info['name']
                    link = info['link']
                    email = get_information(link)
                    if email != None:
                        print("===========[EXTRACT]======================")
                        print(name)
                        print(link)
                        print(email)
                        print("===========[EXTRACT]======================")
                        
                        data = {
                            'email': email,
                            'name': name,
                            'url': link
                        }

                        json_db(data=data)
                        #make_csv(name, email, link)
                except:
                    pass

            print("===========[PROFILES]======================")
        else:
            print("============[FINISH]=====================")
            print(MAIN_URL + str(count))
            print('Termino')
            print("=============[FINISH]====================")
            break


    #driver.get_screenshot_as_file('Page.png')
    driver.quit()
    #print(person_information)

#get_information('http://www.thecounsellorthing.com/')