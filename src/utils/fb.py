from requests import Session
from bs4 import BeautifulSoup
# import google_sheet
import os, sys, time, random, requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from src.types.settings import UserConnectionError
from re import sub

# sys.stdin.reconfigure(encoding='unicode_escape')
# sys.stdout.reconfigure(encoding='unicode_escape')


def get_response(url: str, auth_params: tuple[str], cookie: str = None) -> tuple[requests.Response, str]:
    try:
        if not cookie:
            cookie = login(auth_params[0], auth_params[1])
    except UserConnectionError:
        raise UserConnectionError
    try:
        response = Session().get(url=url, headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Cookie": cookie,  # CHANGE datr

        })
    except:
        response = None
    finally:
        return response, cookie


def get_urls(response: requests.Response) -> list[str]:
    soup = BeautifulSoup(response.text, features='lxml')
    return ['https://www.facebook.com' + a['href'] for a in soup.find_all('a') if '/marketplace/item' in a['href']]


def handle_price(price_: str):
    factor = 1
    if 'тыс' in price_:
        factor *= 1000
    elif 'млн' in price_:
        factor *= 1000000
    elif 'млрд' in price_:
        factor *= 1000000000
    in_month = False if '/месяц' not in price_ else True
    currency = 'rp' if 'rp' in price_.lower() else 'IDR' if 'idr' in price_.lower() else '$' if '$' in price_ else ''
    try:
        price_ = float(''.join([i if i.isdigit() else '.' if i == ',' else '' for i in price_])) * factor
    except ValueError:
        price_ = 0.0
    return price_, currency, in_month


def get_product_info(response: requests.Response, url: str) -> list[str] | None:
    text = response.text
    if 'marketplace_listing_title' not in text:
        return None

    soup = BeautifulSoup(response.text, features='lxml')
    title, description, price, product_prop, profile_url, pdp_fields, images = '', '', '', '', '', [], []
    try:
        spans = soup.find(
            attrs={'class': 'x1jx94hy x78zum5 xdt5ytf x1lytzrv x6ikm8r x10wlt62 xiylbte xtxwg39'}).find_all(
            'span')
        title = spans[2].text

        price = spans[3].text

        price, currency, in_month = handle_price(price)

    except AttributeError:
        try:
            title = text.split('"marketplace_listing_title":"')[1].split('","')[0].encode('utf-8').decode(
                'unicode-escape')
            price = text.split('amount":')[1].split('},')[0].replace('currency":"', ' ').replace(',', '').replace('"',
                                                                                                                  '')
            price, currency, in_month = handle_price(price)
        except IndexError:
            pass

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(text)
    try:
        description = text.split('"redacted_description":{"text":"')[1].split('"}')[0]
        description = repr(description).replace('\\/', '').replace('\\\\n', ' ')
        description = sub(r'\\ud\w{3}', '', description)
        print(description)
    except IndexError:
        pass
    current_datetime = datetime.now()
    try:
        pdp_fields = text.split('"pdp_fields":[')[1].split(']')[0].split('{"display_label":"')
    except IndexError:
        pass
    product_prop = [p.split('"')[0].encode('utf-8').decode('unicode-escape') for p in pdp_fields if p]
    try:
        profile_url = 'https://www.facebook.com/marketplace/profile/' + text.split('"actrs\\":\\"')[1].split('\\",\\"')[
            0]
    except IndexError:
        pass
    try:
        images = soup.find(
            attrs={'class': 'xal61yo x78zum5 xdt5ytf x1iyjqo2 x6ikm8r x10wlt62 x1n2onr6 x4fas0m xcg96fm'}) \
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

    return [url, title, price, ','.join(product_prop), description, profile_url, pictures, current_datetime]


def if_url_active(response):
    text = response.text
    # if 'Это объявление уже неактивно' in text or
    if 'redacted_description' not in text:
        return False


def login(login, password):
    ua = "Mozilla/5.0 (Linux; Android 4.1.2; GT-I8552 Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

    url = 'https://n.facebook.com'
    xurl = url + '/login.php'
    try:
        user = login
        pswd = password
        req = requests.Session()
        req.headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en_US', 'cache-control': 'max-age=0',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
            'user-agent': ua
        })
        with req.get(url) as response_body:
            try:
                inspect = bs(response_body.text, 'html.parser')
                lsd_key = inspect.find('input', {'name': 'lsd'})['value']
                jazoest_key = inspect.find('input', {'name': 'jazoest'})['value']
                m_ts_key = inspect.find('input', {'name': 'm_ts'})['value']
                li_key = inspect.find('input', {'name': 'li'})['value']
                try_number_key = inspect.find('input', {'name': 'try_number'})['value']
                unrecognized_tries_key = inspect.find('input', {'name': 'unrecognized_tries'})['value']
                bi_xrwh_key = inspect.find('input', {'name': 'bi_xrwh'})['value']
            except TypeError:
                print(f'\033[1;31m*** type error with user {login} ***\033[0m')
                raise UserConnectionError  # Пока так. ошибка при m_ts_key None type приходит
            data = {
                'lsd': lsd_key, 'jazoest': jazoest_key,
                'm_ts': m_ts_key, 'li': li_key,
                'try_number': try_number_key,
                'unrecognized_tries': unrecognized_tries_key,
                'bi_xrwh': bi_xrwh_key, 'email': user,
                'pass': pswd, 'login': "submit"}
            response_body2 = req.post(xurl, data=data, allow_redirects=True, timeout=300)
            cookie = str(req.cookies.get_dict())[1:-1].replace("'", "").replace(",", ";").replace(":", "=")
            if 'checkpoint' in cookie:
                sys.exit("\033[1;31mAccount terminated by Facebook!\033[0m")
            elif 'c_user' in cookie:
                with open('cookies.txt', 'a') as file:
                    file.write(f'{cookie}\n')
            else:
                raise UserConnectionError  # отследить, что норм куки не пришли
                # sys.exit("\033[38;5;208mIncorrect details\033[0m")
            return cookie
    except requests.exceptions.ConnectionError:
        sys.exit('No internet')
    except KeyboardInterrupt:
        sys.exit("[+] Stopped!")
