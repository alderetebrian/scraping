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
#chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36")
driver = webdriver.Chrome('chromedriver', options=chrome_options)
MAIN_URL = 'https://gestaltcentre.org.uk/find-a-counsellor-or-therapist/directory-of-bacp-counsellors/'
date = datetime.now().strftime("%Y%m%d-%H%M%S")
CSV_FILE = f'gestaltcentre_output_{date}'


# counsellors, psychotherapists, clinical psychologists

def get_information(url):
    driver.get(url)
    #$x('//*[text() = "Email"]')
    #contenido[0].parentElement.getElementsByTagName('strong')[0]
    contenido = driver.find_elements(By.XPATH, '//*[text() = "Email"]')

    # Nombre y Email
    for item in contenido:
        try:
            content = item.find_elements(By.XPATH, '..')[0]
            name = content.find_elements(By.TAG_NAME, 'strong')[0].text
            email = content.find_elements(By.TAG_NAME, 'a')[0]
            email = email.text
            #email = email.split('mailto:')[1]

            make_csv(name, email, url)

        except Exception as e:
            # print(e)
            pass



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
    get_information(MAIN_URL)
    driver.quit()
