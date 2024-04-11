from datetime import datetime
from json import loads
from math import ceil
from typing import Optional, List

import requests
from requests import post


class VilloScraper:

    def __init__(self, scraper_link: str = "https://villo.asia/api/v1/announcements/search"):
        self.scraper_link = scraper_link
        self.ad_title: Optional[str] = None
        self.ad_link: Optional[str] = None
        self.ad_price_view: Optional[float] = None
        self.ad_price_digit: Optional[float] = None
        self.ad_currency: Optional[str] = None
        self.ad_land: Optional[str] = None
        self.ad_pictures: Optional[List[str]] = None
        self.ad_rooms: Optional[dict] = None
        self.ad_id: Optional[int] = None
        self.ad_description: Optional[str] = None

    def request_data(self):
        headers = {
            "Content-Type": "application/json",
        }

        return post(
                    url=self.scraper_link,
                    headers=headers,
                    data='{"filter":{"commercialTypes":["LONG_TERM_RENT"],"dealType":"RENT","propertyType":"RESIDENTIAL","rentPeriod":"MONTH","extraFeatures":[],"page":1,"statuses":["NEW","PUBLISHED"],"onMap":false,"currency":"USD"},"pageable":{"page":0,"sort":[{"property":"id","direction":"desc"}],"size":77}}'
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
        }

        apartments = self.deserialize_data().get("content")

        ads = []
        for apartment in apartments:
            for prop in apartment.get("rentalPeriods")[0].get("rentalProperties"):
                if apartment.get("rentalPeriods")[0].get("rentalProperties")[0].get("rentPeriod") == "MONTH":
                    # period = apartment.get("rentalPeriods")[0].get("rentalProperties")[0].get("rentPeriod")
                    self.ad_price_view = apartment.get("rentalPeriods")[0].get("rentalProperties")[0].get("price")
                    self.ad_currency = apartment.get("rentalPeriods")[0].get("rentalProperties")[0].get("priceCurrency")
                    break
                else:
                    continue

            if self.ad_currency == "$":
                self.ad_price_digit = ceil(float(self.ad_price_view) / 0.000063)

            self.ad_land = apartment.get("realEstateObject").get("address").get("address1")
            self.ad_rooms = apartment.get("realEstateObject").get("bedrooms")
            self.ad_description = apartment.get("description")
            self.ad_pictures = apartment.get("photos")
            self.ad_id = apartment.get("id")
            self.ad_link = "https://villo.asia/announcement/" + str(ad_id)

            print(self.ad_price_view, self.ad_price_digit, self.ad_link)

            ads.append({
                "villo_id": self.ad_id,
                "link": self.ad_link,
                "title": self.ad_description,
                "price": self.ad_price_digit,
                "rooms": self.ad_rooms,
                "land": self.ad_land,
                "description": self.ad_description,
                "images": self.ad_pictures,
                "created_datetime": datetime.now()
            })

for apartment in apartments:
    # print(apartment)
    for prop in apartment.get("rentalPeriods")[0].get("rentalProperties"):
        if apartment.get("rentalPeriods")[0].get("rentalProperties")[0].get("rentPeriod") == "MONTH":
            # period = apartment.get("rentalPeriods")[0].get("rentalProperties")[0].get("rentPeriod")
            price = apartment.get("rentalPeriods")[0].get("rentalProperties")[0].get("price")
            currency = apartment.get("rentalPeriods")[0].get("rentalProperties")[0].get("priceCurrency")
            break
        else:
            continue

    land = apartment.get("realEstateObject").get("address").get("address1")
    rooms = apartment.get("realEstateObject").get("bedrooms")
    description = apartment.get("description")
    photos = apartment.get("photos")
    ad_id = apartment.get("id")
    product_link = "https://villo.asia/announcement/" + str(ad_id)
    print(product_link)

