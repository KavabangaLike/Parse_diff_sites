import scrapy
from scrapy.http import Response
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
from ujson import loads


# import google_sheet


class FacebookSpider(scrapy.Spider):
    name = 'facebook'

    def start_requests(self):
        with open('links.txt', 'r', encoding='utf-8') as file_r:
            for url in [
                'https://www.facebook.com/marketplace/112356482109204/search?sortBy=creation_time_descend&query=property&exact=false']:
                yield scrapy.Request(url=url.strip(), callback=self.parse_product)

    def start(self, response: Response):
        pass
    def parse_links(self, response: Response, *kwargs):
        soup = BeautifulSoup(response.text, features='lxml')

        links = [a['href'] for a in soup.find_all('a') if '/marketplace/item' in a['href']]

    def parse_product(self, response: Response, *kwargs):
        def to_rus(eng_text: str) -> str:
            convert = [('House', 'Дом'), ('Villa', 'Вилла'), ('bed', 'кровать'), ('bath', 'ванна'),
                       ('square meters', 'м²')]
            for trans in convert:
                eng_text.replace(trans[0], trans[1])
            return eng_text

        title, description, price, area, product_type, rooms, profile_url = '', '', '', '', '', '', ''

        soup = BeautifulSoup(response.text, features='lxml')

        # spans = [span.text for span in soup.find_all('span')]
        # for num, span in enumerate(spans):
        #     if span == 'Информация об объекте недвижимости':
        #         product_type = spans[num + 1].text
        #         rooms = spans[num + 2].text
        #     elif span == 'Группы для покупки и продажи':  # !!!!!!!  REMAKE
        #         price = spans[num + 2].text

        images = soup.find_all('img')
        pictures = []
        for img in images:
            try:
                picture = img['src']
                if (('scontent' in picture and ('960x' in picture or '720x' in picture or 'x540' in picture or
                                                'x720' in picture or 'x960' in picture or '540x' in picture)) or img[
                        'alt'] == 'Фото ' + title) and picture not in pictures:
                    pictures.append(picture)
            except KeyError:
                pass
        pictures_gh = [f'=IMAGE("{i}"; 4; 100; 240)' for i in pictures[:10]]
        pictures = ','.join(pictures)

        current_datetime = datetime.now().strftime("%d.%m %H:%M")

        text: str = response.body.decode()  # .split('define":[["DateFo')[1].split('</script>')[0]
        # description = text.split('"redacted_description":{"text":"')[1].split('"}')[0]
        # title = text.split('"marketplace_listing_title":"')[1].split('","')[0]
        #
        # pdp_fields = text.split('"pdp_fields":[')[1].split(']')[0].split('{"display_label":"')
        # product_params = [to_rus(p.split('"')[0]) for p in pdp_fields if p]
        # print(product_params)
        # # area = text.split('square meters')[0].split('>')[-1] + 'м²'
        # price = text.split('amount":')[1].split('},')[0].replace('currency":"', ' ').replace(',', '').replace('"', '')
        # profile_url = 'https://www.facebook.com/marketplace/profile/' + text.split('"actrs\\":\\"')[1].split('\\",\\"')[0]
        # google_sheet.gh_insert([pictures_gh], 50)
        # print(title)
        # print(price)
        # print(area)
        # print(product_type)
        # print(rooms)
        # print(description)
        # print(profile_url)
        # print(pictures)
        # print(product_link)
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(text)
        # print(text)


