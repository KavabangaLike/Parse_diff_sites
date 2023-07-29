from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import requests
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def parse(link):
    site = link.split('/')[2]

    option = Options()
    option.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=option)
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=option)

    # result = requests.get(link).content
    # print(result)
    # soup = BeautifulSoup(result, 'lxml')

    if site == 'www.vseinstrumenti.ru':
        driver.get(link)
        print(site)
        names = driver.find_elements(By.CLASS_NAME, 'df5X3i')
        print(names)
        # price = soup.find(class_='df5X3i').text
        # return price
