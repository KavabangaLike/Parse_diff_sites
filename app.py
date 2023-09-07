import multiprocessing
import random
from datetime import datetime
from src.utils.fb import get_product_info, get_response, get_urls, if_url_active
from database import pg_insert_product, pg_select_product_links, pg_select_products, pg_select_fb_users, pg_select_links
from time import sleep
from src.handlers import handlers
import asyncio
from config import DELAY_LIMITER
# from uses import urls_for_parser
from src.utils.google_sheet import gh_insert, gh_prepare_data
from random import shuffle
from src.types.settings import UserConnectionError, NoUrlsFromParse
from apify import smartproxy_request, apify_request


def start_parse(fb_search_url: str, auth_params: tuple[str],
                geo: str = None, query: str = None) -> None:
    try:
        response = apify_request(url=fb_search_url)
    except UserConnectionError:
        print(f'\033[1;31m***Cant connect with user {auth_params[0]}***\033[0m')
        sleep(random.uniform(25.0, 45.0))
        raise UserConnectionError
    urls_from_search = get_urls(response)
    if not urls_from_search:
        print(f'\033[1;31m***Parse no links with {auth_params[0]}, {geo, query}***\033[0m')
        sleep(random.uniform(25.0, 45.0))
        raise NoUrlsFromParse
    urls_in_db = [str(i) for i in pg_select_product_links()]
    #print(urls_in_db)
    urls_to_parse = []
    # print(urls_from_search)
    for url in urls_from_search:
        if url[0].split('/')[5].strip() not in urls_in_db:
            urls_to_parse.append((url[0], url[1]))
    #print(urls_to_parse)
    print(f'{datetime.now().strftime("%m/%d/%Y,%H:%M:%S> ")}'
          f'{geo} - '
          f'Total: {len(urls_from_search)} New: {len(urls_to_parse)}'
          f' - {query} - '
          f'User: {auth_params[0]}')
    if urls_to_parse:
        for url in urls_to_parse:
            try:
                data = get_product_info(smartproxy_request(url_to_parse=url[0]), url=url[0])  # - cookie
                # data = get_product_info(get_response(url=url, auth_params=auth_params), url=url)  # - cookie
                # data = get_product_info(get_response(url=url, auth_params=auth_params)[0], url=url)  # - cookie
            except AttributeError:
                print('UserConnectionError')
                raise UserConnectionError

            if data:
                data.append(url[1] + f' ({geo})')
                pg_insert_product(data)

                async def send_data(dat):
                    await handlers.send_all(dat)

                loop = asyncio.get_event_loop()
                coroutine = send_data(data)
                loop.run_until_complete(coroutine)

                sleep(random.uniform(0.045 * DELAY_LIMITER, 0.1 * DELAY_LIMITER))
            else:
                print(f'No incoming data !!! from {url}')
    sleep(random.uniform(3 * DELAY_LIMITER, 5 * DELAY_LIMITER))


def parsing():
    urls_for_parser = pg_select_links()
    # urls_for_parser = ['https://www.facebook.com/marketplace/denpasar/propertyforsale?sortBy=creation_time_descend&query=House%20for%20rent&latitude=-8.5132&longitude=115.263&radius=7',
    #                    'https://www.facebook.com/marketplace/denpasar/propertyforsale?sortBy=creation_time_descend&query=House%20for%20rent&latitude=-8.5132&longitude=115.263&radius=7',]
    fb_users = pg_select_fb_users()
    shuffle(fb_users)
    while ...:
        for fb_user in fb_users:
            i, user_links_count = 0, 0  # индикатор ошибок, счетчик обработанных ссылок
            for link in urls_for_parser.copy():
                urls_for_parser.append(urls_for_parser.pop(0))  # первую ссылку в списке добававляет в конец списка
                while ...:
                    # print(f'<<< Current user is {fb_user[0]} >>>')
                    try:
                        start_parse(fb_search_url=link[0], geo=link[2], query=link[1], auth_params=fb_user)
                    except NoUrlsFromParse:
                        i = 1
                        break
                    except UserConnectionError:
                        print('UserConnectionError')
                        i = 1
                        break
                    else:
                        break
                    finally:
                        user_links_count += 1
                if i == 1 or user_links_count >= 8:
                    break


def gh_clone_db():
    sleep(3500)
    while ...:
        limit, offset = 200, 0
        while ...:
            data = pg_select_products(limit, offset)
            if not data:
                break
            try:
                gh_insert(gh_prepare_data(data), offset + 1, offset + limit + 1)
            except Exception as ex:
                print('\033[1;31mERROR with google sheet: \033[0m', ex)
                break
            offset += limit
            sleep(1)
        print('Clone to google sheet starting sleep...')
        sleep(18000)


if __name__ == "__main__":
    processes = [parsing]
    for process in processes:
        multiprocessing.Process(target=process).start()

