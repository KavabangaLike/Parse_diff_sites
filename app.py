import multiprocessing
import random
from datetime import datetime
from src.utils.fb import get_product_info, get_response, get_urls, if_url_active
from database import pg_insert_product, pg_select_product_links, pg_select_products, pg_select_fb_users, pg_select_links
from time import sleep
from src.handlers import handlers
import asyncio
# from uses import urls_for_parser
from src.utils.google_sheet import gh_insert, gh_prepare_data


def start_parse(fb_search_url: str, auth_params: tuple[str],
                geo: str = None, query: str = None) -> int:
    try:
        response = get_response(fb_search_url, auth_params)
    except ImportError:
        print(f'\033[1;31m***Cant connect with user {auth_params[0]}***\033[0m')
        sleep(random.uniform(25.0, 45.0))
        return 1
    urls_from_search = get_urls(response)
    urls_id_db = pg_select_product_links()
    urls_to_parse = []
    # print(urls_from_search)
    for url in urls_from_search:
        if url.split('/')[5] not in urls_id_db:
            urls_to_parse.append(url)
    print(f'{datetime.now().strftime("%m/%d/%Y,%H:%M:%S> ")}'
          f'{geo} - '
          f'Total: {len(urls_from_search)} New: {len(urls_to_parse)}'
          f' - {query}')
    if urls_to_parse:
        for url in urls_to_parse:
            data = get_product_info(get_response(url, auth_params=auth_params))
            if data:
                data = [url] + data
                pg_insert_product(data)

                async def send_data(dat):
                    await handlers.send_all(dat)

                loop = asyncio.get_event_loop()
                coroutine = send_data(data)
                loop.run_until_complete(coroutine)

                sleep(random.uniform(4, 8))
            else:
                print(f'No incoming data !!! from {url}')
    sleep(random.uniform(300, 500))
    return 0


def parsing():
    urls_for_parser = pg_select_links()
    fb_users, i = pg_select_fb_users(), 0
    while ...:
        for link in urls_for_parser:
            while ...:
                print(f'<<< Current user is {fb_users[i][0]} >>>')
                result = start_parse(fb_search_url=link[0], geo=link[1], query=link[2], auth_params=fb_users[i])
                if result == 0:
                    break
                elif result == 1:
                    i += 1
                if i >= len(fb_users):
                    i = 0


def gh_clone_db():
    sleep(1500)
    while ...:
        limit, offset = 175, 0
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

