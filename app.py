from src.utils.fb import get_product_info, get_response, get_urls
from database import DataBase
from time import sleep

links_from_site = 'https://www.facebook.com/marketplace/112356482109204/search?sortBy=creation_time_descend&query=property&exact=false'

while ...:
    urls = get_urls(get_response(links_from_site))
    urls_from_db = DataBase.get('product_link')
    urls_to_parse = []
    for url in urls:
        if url not in urls_from_db:
            urls_to_parse.append(url)

    if urls_to_parse:
        for url in urls_to_parse:
            data = get_product_info(get_response(url))
            data = [url] + data
            DataBase.post(data)

            sleep(1.5)
    sleep(200)
