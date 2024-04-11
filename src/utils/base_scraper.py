from asyncio import get_event_loop
from datetime import datetime, timedelta
from typing import Optional

from src.database.models import Advertisement
from src.handlers.handlers import send_all


class ScraperResult:
    def __init__(self,
                 ad_id: dict,
                 ad_title: Optional[str] = None,
                 ad_link: Optional[str] = None,
                 ad_price_digit: Optional[float] = None,
                 ad_price_view: Optional[str] = None,
                 ad_currency: Optional[str] = None,
                 ad_land: Optional[str] = None,
                 ad_pictures: Optional[str] = None,  # str where links split by ,
                 ad_rooms: Optional[dict] = None,
                 ad_description: Optional[str] = None
                 ):
        self.ad_id: dict = ad_id
        self.ad_title = ad_title
        self.ad_link = ad_link
        self.ad_price_digit = ad_price_digit
        self.ad_price_view = ad_price_view
        self.ad_currency = ad_currency
        self.ad_land = ad_land
        self.ad_pictures = ad_pictures  # str where links split by ,
        self.ad_rooms = ad_rooms
        self.ad_description = ad_description

    def save(self) -> None:
        with Advertisement.session() as session:
            new_ad = Advertisement(
                **self.ad_id,
                title=self.ad_title,
                price=self.ad_price_digit,
                land=self.ad_land,
                description=self.ad_description,
                rooms=self.ad_rooms,
                images=",".join(self.ad_pictures),
                created_datetime=datetime.now().timestamp()
            )
            session.add(new_ad)
            session.commit()
            session.refresh(new_ad)

    def send(self):
        apartment_to_handle = [
            self.ad_link,
            self.ad_title,
            self.ad_price_digit,
            "None",
            "None",
            "None",
            self.ad_pictures,
            datetime.now() + timedelta(hours=8),
            self.ad_price_view
        ]

        async def send_data(dat):
            await send_all(dat)

        loop = get_event_loop()
        coroutine = send_data(apartment_to_handle)
        loop.run_until_complete(coroutine)
