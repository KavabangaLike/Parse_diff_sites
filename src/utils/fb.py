from datetime import datetime
from random import randint
import requests
from requests import Session
from bs4 import BeautifulSoup
# import google_sheet

cook = [
    # "wd=1696x418; dpr=1.1320754716981132; datr=xKHAZMuWnirV4_oELBK16644; fr=0gXr1AXvBA3q8xAvG.AWUfXJMtkOHfcgsDwKpKAj87_5E.BkyPNZ.ph.AAA.0.0.BkyPNZ.AWVcuq7G3xU; sb=7KHAZNrUuGwzJZTgwt3hcTFV; locale=ru_RU; c_user=100095339734259; xs=26%3AuLcSlqwfkazF0A%3A2%3A1690883593%3A-1%3A-1%3A%3AAcVDW2AvCWBL4EHzxVzJLxc9ey3Jqh4B66ADN1yzUQ; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1690894265223%2C%22v%22%3A1%7D",  # CHANGE datr
    # "wd=1696x418; dpr=1.1320754716981132; datr=xKHAZMuWnirV4_oELBK1Irg5; fr=0aP5P7Ca0Gy4URFj7.AWXKHf9zk-e08ynMG_v0EMiGja8.BkyNLe.ph.AAA.0.0.BkyNYJ.AWUl5owruPM; sb=7KHAZNrUuGwzJZTgwt3hcTFV; locale=ru_RU; c_user=100095339734259; xs=26%3AuLcSlqwfkazF0A%3A2%3A1690883593%3A-1%3A-1; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1690886632684%2C%22v%22%3A1%7D",  # CHANGE datr
    # "wd=1200x940; dpr=1.5; datr=2234314W334V3234453452; fr=324532532452345zk-e08ynMG_v0EMiGja8.BkyNLe.ph.AAA.0.0.BkyNYJ.AWUl5owruPM; sb=7KHAZNrUuGwzJZTgwt3hcTFV; locale=ru_RU; c_user=100095339734259; xs=26%3AuLcSlqwfkazF0A%3A2%3A1690883593%3A-1%3A-1;",
    "dpr=1.25; datr=c3fHZAUGJZDFg_ip2Flh6699; wd=920x1080",  # CHANGE datr
]


def get_response(url: str, cookie: str = cook[0]) -> requests.Response:
    proxies = {
        'http': 'http://27.254.217.116:8081'
    }
    try:
        response = Session().get(url=url, headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Cookie": cookie,  # CHANGE datr

        })
    except:
        response = None
    finally:
        return response


def get_urls(response: requests.Response) -> list[str]:
    soup = BeautifulSoup(response.text, features='lxml')
    return ['https://www.facebook.com' + a['href'] for a in soup.find_all('a') if '/marketplace/item' in a['href']]


def get_product_info(response: requests.Response) -> list[str] | None:
    text = response.text
    if 'marketplace_listing_title' not in text:
        return None

    soup = BeautifulSoup(response.text, features='lxml')
    title, description, price, product_prop, profile_url, pdp_fields, images = '', '', '', '', '', [], []
    try:
        spans = soup.find(attrs={'class': 'x1jx94hy x78zum5 xdt5ytf x1lytzrv x6ikm8r x10wlt62 xiylbte xtxwg39'}).find_all(
            'span')
        title = spans[2].text
        price = spans[3].text
    except AttributeError:
        try:
            title = text.split('"marketplace_listing_title":"')[1].split('","')[0].encode('utf-8').decode(
                'unicode-escape')
            price = text.split('amount":')[1].split('},')[0].replace('currency":"', ' ').replace(',', '').replace('"', '')

        except IndexError:
            pass

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(text)
    try:
        description = text.split('"redacted_description":{"text":"')[1].split('"}')[0]
    except IndexError:
        pass
    current_datetime = datetime.now().strftime("%d.%m %H:%M")
    try:
        pdp_fields = text.split('"pdp_fields":[')[1].split(']')[0].split('{"display_label":"')
    except IndexError:
        pass
    product_prop = [p.split('"')[0].encode('utf-8').decode('unicode-escape') for p in pdp_fields if p]
    try:
        profile_url = 'https://www.facebook.com/marketplace/profile/' + text.split('"actrs\\":\\"')[1].split('\\",\\"')[0]
    except IndexError:
        pass
    try:
        images = soup.find(attrs={'class': 'xal61yo x78zum5 xdt5ytf x1iyjqo2 x6ikm8r x10wlt62 x1n2onr6 x4fas0m xcg96fm'})\
            .find_all('img')
    except AttributeError:
        pass
    pictures = []
    for img in images:
        try:
            picture = img['src']
            if picture not in pictures:
                pictures.append(picture)
        except KeyError:
            pass
    pictures_google = [f'=IMAGE("{i}"; 4; 100; 240)' for i in pictures[:10]]
    pictures = ','.join(pictures)
    # google_sheet.gh_insert([pictures_gh], 50)
    # print(title)
    # print(price)
    # print(product_prop)
    # print(description)
    # print(profile_url)
    # print(pictures)
    # print(url)
    return [title, price, ','.join(product_prop), description, profile_url, pictures, current_datetime]


def if_url_active(response):
    text = response.text
    # if 'Это объявление уже неактивно' in text or
    if 'redacted_description' not in text:
        return False


