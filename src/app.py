import asyncio
import random
from datetime import datetime
from random import shuffle
from time import sleep

from src.database.database_func import pg_insert_product, pg_select_product_links, pg_select_links
from src.handlers import handlers
from src.settings import DELAY_LIMITER
from src.utils.fb import products_from_search
from src.utils.web_api_services import smartproxy_request
from src.validation.settings import UserConnectionError, NoUrlsFromParse


def async_tg_send(data):
    async def send_data(dat):
        await handlers.send_all(dat)

    loop = asyncio.get_event_loop()
    coroutine = send_data(data)
    loop.run_until_complete(coroutine)


def parse_search_only(fb_search_url: str, geo: str):
    try:
        response = smartproxy_request(url_=fb_search_url)
    except Exception as ex:
        print(datetime.now(), "Connection Error××××××××××××")
        print(ex)
        sleep(random.uniform(50.0, 140.0))
        raise NoUrlsFromParse

    try:
        urls_from_search = products_from_search(page=response)
    except:
        print("No LINKS")
        sleep(random.uniform(100.0, 175.0))
        raise NoUrlsFromParse

    if not urls_from_search:
        print(f'\033[1;31m***Parse no links, {geo}***\033[0m')
        sleep(random.uniform(25.0, 45.0))
        raise NoUrlsFromParse

    urls_in_db = [str(i) for i in pg_select_product_links()]
    urls_to_parse = []
    for url_data in urls_from_search:
        if url_data[0].split('/')[5].strip() not in urls_in_db:
            urls_to_parse.append(url_data)

    print(f'{datetime.now().strftime("%m/%d/%Y,%H:%M:%S> ")}'
          f'{geo} - '
          f'Total: {len(urls_from_search)} New: {len(urls_to_parse)}')

    if urls_to_parse:
        for data in urls_to_parse:
            data[-1] = data[-1] + f' ({geo})'
            pg_insert_product(data)

            async_tg_send(data=data)

    sleep(random.uniform(DELAY_LIMITER * 0.9, DELAY_LIMITER * 1.3))


def parsing():
    urls_for_parser = pg_select_links()
    shuffle(urls_for_parser)
    for link in urls_for_parser:
        try:
            parse_search_only(fb_search_url=link[0], geo=link[2])
        except NoUrlsFromParse:
            print('No Urls From Parse !!!')
            break
        except UserConnectionError:
            print('UserConnectionError')
            break
