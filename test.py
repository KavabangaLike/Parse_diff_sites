from datetime import datetime, timedelta

import requests
import json

from bs4 import BeautifulSoup

from apify import apify_request


def products_from_search(page: str) -> list[list]:
    soup = BeautifulSoup(page, features='lxml')
    blocks = soup.find_all(attrs={
        'class': 'x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24'})
    ads_data = []
    for block in blocks:
        try:
            if block.find('a')['href']:
                product_link = 'https://www.facebook.com' + block.find('a')['href'].replace('&__tn__=!%3AD', '')
                geolocation = block.find_all('span')[6].text
                price = block.find_all('span')[2].text
                title = block.find_all('span')[4].text
                current_datetime = datetime.now() + timedelta(hours=8)
                image = block.find('img')['src']
                for n, i in enumerate(block.find_all('span')):
                    print(n, i.text)
                ads_data.append([product_link, title, [i for i in price if i.isdigit()], 'None from search', 'None from search', 'None from search', image, current_datetime, price, geolocation])
        except TypeError:
            pass
    return ads_data


print(products_from_search(page=apify_request(url='https://www.facebook.com/marketplace/denpasar/propertyforsale?sortBy=creation_time_descend&query=House%20for%20rent&latitude=-8.5132&longitude=115.263&radius=7')))
