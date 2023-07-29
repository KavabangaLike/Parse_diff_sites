from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineKeyboards:
    def __init__(self, url1, url2):
        self.url1 = url1
        self.url2 = url2

    def product_more_buttons(self):
        ikb1 = InlineKeyboardButton(text='Подробнее', url=self.url1)
        ikb2 = InlineKeyboardButton(text='Продавец', url=self.url2)
        return InlineKeyboardMarkup().add(ikb2, ikb1)

