# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from pydantic import PositiveInt
from typing import Optional, Literal


class UserCallbackData(CallbackData, prefix='us'):
    user_id: PositiveInt
    group: Literal['admins', 'users', 'newbies']
    period: Literal['week', '1month', '3month', 'forever', 'day', 'fault']


class UserFilterCallbackData(CallbackData, prefix='er'):
    user_id: PositiveInt
    filter_name: Optional[str]
    type_: PositiveInt
    action: Literal['back', 'next', None]


class InlineKeyboards:
    def __init__(self, param1=None, param2=None, param3=None, param4=None):
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.param4 = param4

    def product_more_buttons(self) -> InlineKeyboardMarkup:
        ikb1 = InlineKeyboardButton(text='Подробнее', url=self.param1)
        # ikb2 = InlineKeyboardButton(text='Продавец', url=self.param2)
        return InlineKeyboardMarkup(inline_keyboard=[[ikb1]])

    def handle_user(self) -> InlineKeyboardMarkup:
        ikb_group = [
            InlineKeyboardButton(text='ADMINS', callback_data=UserCallbackData(group='admins', user_id=self.param1, period=self.param3).pack()),
            InlineKeyboardButton(text='USERS', callback_data=UserCallbackData(group='users', user_id=self.param1, period=self.param3).pack()),
            InlineKeyboardButton(text='NEWBIES', callback_data=UserCallbackData(group='newbies', user_id=self.param1, period=self.param3).pack()),
            ]
        ikb_period = [
            InlineKeyboardButton(text='♾', callback_data=UserCallbackData(period='forever', user_id=self.param1, group=self.param2).pack()),
            InlineKeyboardButton(text='3 MO.', callback_data=UserCallbackData(period='3month', user_id=self.param1, group=self.param2).pack()),
            InlineKeyboardButton(text='MO.', callback_data=UserCallbackData(period='1month', user_id=self.param1, group=self.param2).pack()),
            InlineKeyboardButton(text='WE.', callback_data=UserCallbackData(period='week', user_id=self.param1, group=self.param2).pack()),
            InlineKeyboardButton(text='✖️', callback_data=UserCallbackData(period='fault', user_id=self.param1, group=self.param2).pack()),
        ]
        for button in ikb_group + ikb_period:
            button.text.replace(' ✅', '')
        for b in ikb_group:
            if self.param2 in b.callback_data:
                b.text += ' ✅'
        for b in ikb_period:
            if self.param3 in b.callback_data:
                b.text += '✅'
        return InlineKeyboardMarkup(inline_keyboard=[ikb_group, ikb_period])

    def user_filter(self):
        ikb = []
        for facility in self.param1:
            b = InlineKeyboardButton(text=facility, callback_data=UserFilterCallbackData(filter_name=facility, user_id=self.param3, type_=self.param4, action=None).pack())
            ikb.append([b])
            if facility in self.param2:
                b.text += ' ✅'
        ikb.append([
            InlineKeyboardButton(text='Далее', callback_data='next'),
            InlineKeyboardButton(text='Назад', callback_data='Назад'),
        ])
        return InlineKeyboardMarkup(inline_keyboard=ikb)
