# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from pydantic import PositiveInt
from typing import Optional, Literal


class UserGroupCallbackData(CallbackData, prefix='us'):
    user_id: PositiveInt
    group: Literal['admins', 'users', 'newbies']


class InlineKeyboards:
    def __init__(self, param1=None, param2=None):
        self.param1 = param1
        self.param2 = param2

    def product_more_buttons(self) -> InlineKeyboardMarkup:
        ikb1 = InlineKeyboardButton(text='Подробнее', url=self.param1)
        # ikb2 = InlineKeyboardButton(text='Продавец', url=self.param2)
        return InlineKeyboardMarkup(inline_keyboard=[[ikb1]])

    def handle_user(self) -> InlineKeyboardMarkup:
        ikb = [
            InlineKeyboardButton(text='ADMINS', callback_data=UserGroupCallbackData(group='admins', user_id=self.param1).pack()),
            InlineKeyboardButton(text='USERS', callback_data=UserGroupCallbackData(group='users', user_id=self.param1).pack()),
            InlineKeyboardButton(text='NEWBIES', callback_data=UserGroupCallbackData(group='newbies', user_id=self.param1).pack()),
        ]
        for button in ikb:
            button.text.replace(' ✅', '')
        for b in ikb:
            if self.param2 in b.text.lower():
                b.text += ' ✅'
        return InlineKeyboardMarkup(inline_keyboard=[ikb])
