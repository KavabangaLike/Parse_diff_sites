from asyncio import get_event_loop
from datetime import datetime, timedelta
from random import uniform
from time import sleep

from requests import post
from orjson import loads
from sqlalchemy import select

from config import DELAY_LIMITER
from src.database.models import BProduct
from src.handlers.handlers import send_all
from math import ceil


class BalivingScraper:
    def __init__(self, scraper_link="https://tersvdkiy8.execute-api.eu-central-1.amazonaws.com/prod/tools-runner"):
        self.scraper_link = scraper_link

    def request_data(self) -> str:
        return post(
            url=self.scraper_link,
            json={"tool_id":"1ebc1158-0299-4f2f-9733-c0b99f22b400","profile":{"login":"undefined"},"project_id":"1468532","referer":"https://baliving.ru","user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0","filters":None,"offset":None}

        ).content

    def deserialize_data(self) -> dict:
        return loads(self.request_data())

    def parse_data(self) -> list[dict]:
        lands = {
            "Чангу": "Changgu",
            "Убуд": "Ubud",
            "Санур": "Sanur",
            "Табанан": "Tabanan",
            "Унгасан": "Ungasan",
            # "Умалас": "Umalas",
            # "Семиньяк": "Seminyak",
            # "Джимбаран": "JimBaran",
            # "Нуса Дуа": "Nusa Dua",
        }
        res_lst = []
        for apartment in self.deserialize_data().get("records"):
            apartment_data = apartment.get("card_description").split("**")
            try:
                res_lst.append({
                    "id": apartment.get("id"),
                    "link": "https://baliving.ru" + apartment.get("button_link_prod"),
                    "title": apartment.get("card_description"),
                    "price": apartment.get("price"),
                    "rooms": apartment_data[4],
                    "land": lands[apartment_data[2].strip()],
                    "description": apartment.get("popup_text").split("Цена в месяц:**")[1].split("<")[0],
                    "images": apartment.get("image_list")

                })
            except KeyError:
                continue
        return res_lst

    def handle_data(self) -> None:
        while ...:
            apartments, apartments_new = self.parse_data(), []
            with BProduct.session() as session:
                apartments_exist = session.scalars(select(BProduct.id)
                                                   .filter(BProduct.id.in_([i.get("id") for i in apartments])))
            apartments_exist = [*apartments_exist]
            for apartment in apartments:
                if not (apartment.get("id") in apartments_exist):
                    apartments_new.append(apartment)

            print(f'{datetime.now().strftime("%m/%d/%Y,%H:%M:%S> Baliving")}'
                  f'Total: {len(apartments)} New: {len(apartments_new)}')

            if apartments_new:
                apartments_new = apartments_new[:3]  # Берем первые 13, чтобы не спамить в тг
                products = []
                with BProduct.session() as session:
                    for apartment in apartments_new:
                        b_product = BProduct(**apartment)
                        products.append(b_product)
                    session.add_all(products)
                    session.commit()

                for apartment in apartments_new:
                    rp_price = ceil(float(apartment.get("price")) / 0.000063)
                    apartment_to_handle = [
                            apartment.get("link"),
                            apartment.get("title").replace("**", "").strip() + "\n" + apartment.get("description")+ f"{apartment.get('rooms').strip()} kt",
                            rp_price,
                            "None",
                            "None",
                            "None",
                            ",".join(apartment.get("images")[:-1]),
                            datetime.now() + timedelta(hours=8),
                            str(apartment.get("price")) + f"$ ({rp_price} rp)",
                            " (" + apartment.get("land") + ")"
                        ]


                    async def send_data(dat):
                        await send_all(dat)

                    loop = get_event_loop()
                    coroutine = send_data(apartment_to_handle)
                    loop.run_until_complete(coroutine)

            sleep(uniform(1 * DELAY_LIMITER, 3 * DELAY_LIMITER))
BalivingScraper().handle_data()