import datetime
import random
import threading
import sqlite3
import uuid

from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import quickstart

driver = webdriver.Firefox()
driver.options = FirefoxOptions()
cx = sqlite3.connect('db.sqlite3')
cu = cx.cursor()

def enter_facebook() -> None:
    email = '+375292466147'
    password = 'barakuda007'

    driver.get('https://www.facebook.com/login/')

    email_xpath = '//*[@id="email"]'
    pass_xpath = '//*[@id="pass"]'
    but_xpath = '//*[@id="loginbutton"]'

    email_element = driver.find_element('xpath', email_xpath)
    pass_element = driver.find_element('xpath', pass_xpath)
    but_element = driver.find_element('xpath', but_xpath)

    email_element.send_keys(email)
    pass_element.send_keys(password)
    but_element.click()
    sleep(1)


def get_product_links() -> list[str]:
    f = driver.find_elements(By.TAG_NAME, 'a')

    required_links = []
    for i in f:
        link = i.get_property('href')
        if 'item' in link:
            required_links.append(i.get_property('href'))

    print(required_links)
    print(len(required_links))
    return required_links


def get_product_info(product_link):

    driver.get(product_link)
    sleep(2)
    try:
        driver.find_element(By.CSS_SELECTOR,
                            '.x126k92a > div:nth-child(1) > span:nth-child(1) > div:nth-child(1)').click()
    except Exception as ex:
        pass

    title, description, price, area, product_type, rooms, profile_url = '', '', '', '', '', '', ''

    spans = []
    for span in driver.find_elements(By.TAG_NAME, 'span'):
        try:
            if span.text.strip():
                spans.append(span)
        except Exception as ex:
            # print(ex)
            pass

    for c, span in enumerate(spans):

        try:
            txt = span.text.strip()
            print(f'{c}-----------------------------------------------------------')
            print(txt)
            if txt == 'Информация об объекте недвижимости':
                product_type = spans[c + 1].text
                rooms = spans[c + 2].text
            elif txt == 'Группы для покупки и продажи':  # !!!!!!!  REMAKE
                title = spans[c + 1].text
                price = spans[c + 2].text
            elif 'м²' in txt:
                area = txt
            elif txt == 'Подробнее':
                description = spans[c + 7].text.replace('Свернуть', '')
            elif txt == 'Описание':
                description = spans[c + 2].text.replace('Свернуть', '')
                break
        except Exception as ex:
            # print(ex)
            pass

    images = driver.find_elements(By.TAG_NAME, 'img')
    pictures = []
    for img in images:
        picture = img.get_property('src')
        if (('scontent' in picture and ('960x' in picture or '720x' in picture or 'x540' in picture or
                                      'x720' in picture or 'x960' in picture or '540x' in picture)) or img.get_property('alt') == 'Фото ' + title) and picture not in pictures:
            pictures.append(picture)
    pictures = ','.join(pictures)

    profile_urls = [i.get_property('href') for i in driver.find_elements(By.TAG_NAME, 'a') if
                    'profile' in i.get_property('href') and '100095339734259' not in i.get_property('href')]
    if profile_urls:
        profile_url = profile_urls[0]

    current_datetime = datetime.datetime.now().strftime("%d.%m %H:%M")

    print(title)
    print(price)
    print(area)
    print(product_type)
    print(rooms)
    print(description)
    print(profile_url)
    print(pictures)
    print(product_link)

    sleep(3)
    return [product_link, title, price, area, product_type, rooms, description, profile_url, pictures, current_datetime]


def scroll_site(tac):
    # driver.get('https://www.facebook.com/marketplace/107677462599905/search?query=property')
    curr_count, tic = 0, 0
    while tic <= tac:
        print(tic, tac)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)
        links_count = len(driver.find_elements(By.TAG_NAME, 'a'))
        if links_count <= curr_count:
            break
        curr_count = links_count
        tic += 1
    return None

p = [
        'https://www.facebook.com/marketplace/item/236635722648465/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A6f8e9fe4-663f-4b0f-b286-e74aa8e96906',
        'https://www.facebook.com/marketplace/item/193978449730162/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A42548dfa-3503-4370-89dc-9783d40c0f3c&__tn__=!%3AD',
        'https://www.facebook.com/marketplace/item/1401182314028926/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A42548dfa-3503-4370-89dc-9783d40c0f3c&__tn__=!%3AD',
        'https://www.facebook.com/marketplace/item/3681456175458187/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A42548dfa-3503-4370-89dc-9783d40c0f3c&__tn__=!%3AD',
        'https://www.facebook.com/marketplace/item/3481097948816317/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A42548dfa-3503-4370-89dc-9783d40c0f3c&__tn__=!%3AD',
        'https://www.facebook.com/marketplace/item/2188630028004198/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A42548dfa-3503-4370-89dc-9783d40c0f3c&__tn__=!%3AD',
        'https://www.facebook.com/marketplace/item/3051821154960038/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A42548dfa-3503-4370-89dc-9783d40c0f3c&__tn__=!%3AD',
        'https://www.facebook.com/marketplace/item/717740099813620/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A42548dfa-3503-4370-89dc-9783d40c0f3c&__tn__=!%3AD',
        'https://www.facebook.com/marketplace/item/543151604269003/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A42548dfa-3503-4370-89dc-9783d40c0f3c&__tn__=!%3AD',
        'https://www.facebook.com/marketplace/item/201931492415348/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A42548dfa-3503-4370-89dc-9783d40c0f3c&__tn__=!%3AD',
        'https://www.facebook.com/marketplace/item/904386110787244/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A42548dfa-3503-4370-89dc-9783d40c0f3c&__tn__=!%3AD'
]

while ...:
    # enter_facebook()
    # driver.get(
    #     'https://www.facebook.com/marketplace/112356482109204/search?sortBy=creation_time_descend&query=house%20for%20sale&exact=false'
    # )
    # scroll_site(2)
    # links = get_product_links()
    # with open('links.txt', 'w', encoding='utf-8') as file_w:
    #     for link in links:
    #         file_w.write(f'{link}\n')
    # break
    #
    with open('links.txt', 'r', encoding='utf-8') as file_r:
        links = file_r.read().split('\n')
    enter_facebook()
    for url in links:
        sql_insert = 'INSERT INTO products(id, product_link, title, price, area, product_type, rooms, description, profile_url, pictures, current) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        data = get_product_info(url)
        cu.execute(sql_insert, (random.randint(123, 32542), data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9]))
        cx.commit()
        sleep(4)


# enter_facebook()
# data = [["id", "product_link", 'title', 'price', 'area', 'product_type', 'rooms', 'description', 'profile_url', 'pictures', 'is_active']]
# for c, url in enumerate(p):
#     product = [str(i) for i in get_product_info(url)]
#     product.insert(0, str(c + 1))
#     data.append(product)
#
#     quickstart.gh_insert([product], c + 2)
