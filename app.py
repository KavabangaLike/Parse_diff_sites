import random

from src.utils.fb import get_product_info, get_response, get_urls, if_url_active
from database import DataBase, pg_insert_product, pg_select_product_links
from time import sleep
from src.handlers import handlers
import asyncio

fb_search_urls = [
    'https://www.facebook.com/marketplace/112356482109204/search/?sortBy=creation_time_descend&query=property&exact=false',
    'https://www.facebook.com/marketplace/112356482109204/search?query=rent%20villa',
    'https://www.facebook.com/marketplace/109241542435052/search/?sortBy=creation_time_descend&query=property&exact=false',
    'https://www.facebook.com/marketplace/philly/search/?sortBy=creation_time_descend&query=property&exact=false',
    'https://www.facebook.com/marketplace/guatemalacity/search/?query=rent%20villa&exact=false',
    'https://www.facebook.com/marketplace/lisbon/search/?query=rent%20villa&exact=false']


def start_parse(fb_search_url: str) -> None:
    urls_from_search = get_urls(get_response(fb_search_url))
    urls_id_db = pg_select_product_links()
    urls_to_parse = []
    # print(urls_from_search)
    for url in urls_from_search:
        if url.split('/')[5] not in urls_id_db:
            urls_to_parse.append(url)
    print(f'Найдено объявлений: {len(urls_from_search)} Найдено новых объявлений: {len(urls_to_parse)}')
    if urls_to_parse:
        for url in urls_to_parse:
            data = get_product_info(get_response(url))
            if data:
                data = [url] + data
                pg_insert_product(data)
                # DataBase.post_product(data)

                async def send_data(dat):
                    await handlers.send_all(dat)

                loop = asyncio.get_event_loop()
                coroutine = send_data(data)
                loop.run_until_complete(coroutine)

                sleep(random.uniform(2.0, 6.0))
            else:
                print(f'No incoming data !!! from {url}')
    sleep(random.uniform(25.0, 45.0))
        #     tic += 1
        #
        # urls_to_check = DataBase.get('product_link', 'products WHERE is_active=1')
        # for url in urls_to_check:
        #     if_url_active(get_response(url))
        # sleep(50)


def main():
    while ...:
        for link in fb_search_urls:
            start_parse(link)


if __name__ == '__main__':
    main()



# def main():
#     threads = []
#     for url in fb_search_urls:
#         thread = threading.Thread(target=start_parse, args=[url])
#         threads.append(thread)
#         thread.start()
#
#     for thread in threads:
#         thread.join()