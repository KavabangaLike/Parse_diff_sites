from requests import Session
from bs4 import BeautifulSoup
# import google_sheet
import os, sys, time, random, requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from src.validation.settings import UserConnectionError
from re import sub

# sys.stdin.reconfigure(encoding='unicode_escape')
# sys.stdout.reconfigure(encoding='unicode_escape')


def get_response(url: str, auth_params: tuple[str], cookie: str = None, proxies=None):
    # proxies = {'https': 'http://yfonarev2020:66ccakAzi7@185.33.85.249:51523'}
    try:
        if not cookie:
            cookie = login(auth_params[0], auth_params[1])
    except UserConnectionError:
        raise UserConnectionError
    try:
        response = Session().get(url=url, headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": 'en_US', 'cache-control': 'max-age=0',  # "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Cookie": cookie,  # CHANGE datr

        })
    except:
        response = None
    finally:
        return response.text


def get_urls(response: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(response, features='lxml')
    # print(response)
    blocks = soup.find_all(attrs={
        'class': 'x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24'})
    links_and_geo = []
    for block in blocks:
        try:
            if block.find('a')['href']:
                links_and_geo.append(('https://www.facebook.com' + block.find('a')['href'].replace('&__tn__=!%3AD', ''), block.find_all('span')[6].text))
        except TypeError:
            pass
    return links_and_geo


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
                digit_price = ''.join([i for i in price if i.isdigit()])
                if digit_price:
                    digit_price = float(digit_price)
                else:
                    digit_price = 0.0
                # print(digit_price)
                ads_data.append([product_link, title, digit_price,
                                 'None from search', 'None from search', 'None from search', image, current_datetime,
                                 price, geolocation])
        except TypeError:
            pass
    return ads_data


def handle_price(price_: str):
    factor = 1
    if 'тыс' in price_ or 'K' in price_:
        factor *= 1000
    elif 'млн' in price_ or 'M' in price_:
        factor *= 1000000
    elif 'млрд' in price_ or 'B' in price_:
        factor *= 1000000000
    in_month = False if '/месяц' not in price_ else True
    currency = 'rp' if 'rp' in price_.lower() else 'IDR' if 'idr' in price_.lower() else '$' if '$' in price_ else ''
    try:
        price_ = float(''.join([i if i.isdigit() else '.' if i == ',' else '' for i in price_])) * factor
    except ValueError:
        price_ = 0.0
    return price_, currency, in_month


def get_product_info(response, url: str) -> list[str] | None:
    text = response
    # if 'marketplace_listing_title' not in text:
    #     return None

    soup = BeautifulSoup(response, features='lxml')
    title, description, price, product_prop, profile_url, pdp_fields, images, full_price = '', '', 0.0, '', '', [], [], ''
    try:
        spans = soup.find(
            attrs={'class': 'x1jx94hy x78zum5 xdt5ytf x1lytzrv x6ikm8r x10wlt62 xiylbte xtxwg39'}).find_all(
            'span')
        title = spans[2].text

        price_text = spans[3].text

        price, currency, in_month = handle_price(price_text)
        full_price = (str(int(price)) + ' ' + currency)[::-1].replace('000000000', 'noillib ').replace('000000', 'nlm ')\
            .replace('000', 'dnasuoht ')[::-1]
    except AttributeError:
        try:
            title = text.split('"marketplace_listing_title":"')[1].split('","')[0].encode('utf-8').decode(
                'unicode-escape')
            price = text.split('amount":')[1].split('},')[0].replace('currency":"', ' ').replace(',', '').replace('"',
                                                                                                                  '')
            full_price = price
            price, currency, in_month = handle_price(price)
        except IndexError:
            pass
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(text)
    try:
        description = text.split('"redacted_description":{"text":"')[1].split('"}')[0]
        description = description.encode('raw_unicode_escape').decode('unicode_escape').encode('utf-16_BE','surrogatepass').decode('utf-16_BE')
        # description = repr(description).replace('\\/', '').replace('\\\\n', ' ')
        # description = sub(r'\\u\w{4}', '', description)  # удалить юникод символы
    except IndexError:
        pass
    current_datetime = datetime.now() + timedelta(hours=8)
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

    return [url, title, price, ','.join(product_prop), description, profile_url, pictures, current_datetime, full_price]


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
                print(f'\033[1;31m***Account terminated by Facebook!***\033[0m')
                raise UserConnectionError
            elif 'c_user' in cookie:
                with open('cookies.txt', 'a') as file:
                    file.write(f'{cookie}\n')
            else:
                raise UserConnectionError  # отследить, что норм куки не пришли
                # sys.exit("\033[38;5;208mIncorrect details\033[0m")
            return cookie
    except requests.exceptions.ConnectionError:
        print(f'\033[1;31m*** No internet ***\033[0m')
        raise UserConnectionError
    except KeyboardInterrupt:
        sys.exit("[+] Stopped!")
