import random
from datetime import datetime
from src.utils.fb import get_product_info, get_response, get_urls, if_url_active
from database import DataBase, pg_insert_product, pg_select_product_links
from time import sleep
from src.handlers import handlers
import asyncio
from uses import urls_for_parser


def start_parse(fb_search_url: str, cookie: str, geo: str = None, query: str = None) -> None:
    urls_from_search = get_urls(get_response(fb_search_url, cookie=cookie))
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
            data = get_product_info(get_response(url, cookie=cookie))
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


def main():
    while ...:
        for link in urls_for_parser:
            start_parse(link[2], link[3], link[0], link[1])


if __name__ == "__main__":
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