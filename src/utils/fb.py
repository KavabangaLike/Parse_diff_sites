import time
from datetime import datetime
from requests import Session
from bs4 import BeautifulSoup
# import google_sheet


def get_response(url):
    response = Session().get(url=url, headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Cookie": "wd=1036x739; datr=z4nCZKF-sdrRMplv6IhIbFHr; fr=0cxIebMfLwmGCNJWj.AWWoP9Cz4w_a-LHnFdE7MGCavFs.BkworY.6b.AAA.0.0.BkxtQx.AWW5eDSve-8; dpr=1.25; sb=7F3FZO0sgIfcfmts9EvPeyvt; m_pixel_ratio=1; c_user=100095339734259; xs=18%3A96nNVzRru0y_NA%3A2%3A1690752050%3A-1%3A-1"

    })
    return response


def get_urls(response):
    soup = BeautifulSoup(response.text, features='lxml')

    return ['https://www.facebook.com' + a['href'] for a in soup.find_all('a') if '/marketplace/item' in a['href']]


def get_product_info(response):

    # def to_rus(eng_text: str) -> str:
    #     convert = [('House', 'Дом'), ('Villa', 'Вилла'), ('bed', 'кровать'), ('bath', 'ванна'),
    #                ('square meters', 'м²')]
    #     for trans in convert:
    #         eng_text.replace(trans[0], trans[1])
    #     return eng_text

    soup = BeautifulSoup(response.text, features='lxml')

    title, description, price, product_prop, profile_url, pdp_fields = '', '', '', '', '', []

    text = response.text
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(text)
    try:
        description = text.split('"redacted_description":{"text":"')[1].split('"}')[0]
    except IndexError:
        return None
    title = text.split('"marketplace_listing_title":"')[1].split('","')[0].encode('utf-8').decode('unicode-escape')
    current_datetime = datetime.now().strftime("%d.%m %H:%M")
    try:
        pdp_fields = text.split('"pdp_fields":[')[1].split(']')[0].split('{"display_label":"')
    except IndexError:
        pass
    product_prop = [p.split('"')[0].encode('utf-8').decode('unicode-escape') for p in pdp_fields if p]
    # area = text.split('square meters')[0].split('>')[-1] + 'м²'
    price = text.split('amount":')[1].split('},')[0].replace('currency":"', ' ').replace(',', '').replace('"', '')
    profile_url = 'https://www.facebook.com/marketplace/profile/' + text.split('"actrs\\":\\"')[1].split('\\",\\"')[0]

    images = soup.find(attrs={'class': 'xal61yo x78zum5 xdt5ytf x1iyjqo2 x6ikm8r x10wlt62 x1n2onr6 x4fas0m xcg96fm'})\
        .find_all('img')
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



# while ...:
# for link in ['https://www.facebook.com/marketplace/item/543151604269003/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A42548dfa-3503-4370-89dc-9783d40c0f3c']:
#     print(get_product_info(get_response(link)))
    # time.sleep(100)