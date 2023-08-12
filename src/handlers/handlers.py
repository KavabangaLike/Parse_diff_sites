import aiogram.exceptions
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from aiogram.types.input_media_photo import InputMediaPhoto
from src.settings import bot, dp
from database import pg_insert_new_user, pg_select_all_users_id, pg_change_user_group, pg_change_user_access_period
from src.keyboards.inline.ik import InlineKeyboards, UserCallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from datetime import datetime, timedelta
from aiogram import F


async def send_all(data: list[str]) -> None:
    photos = data[6].split(',')[:10]
    input_media_photos = [InputMediaPhoto(media=url) for url in photos]
    users = pg_select_all_users_id(['users', 'admins', 'superadmins', 'newbies'])
    list_of_prop = [data[2]]
    list_of_prop.extend(data[3].split(','))
    descr = data[4].replace('\\n', ' ').replace('\\/', '/')
    for id in users:
        try:
            try:
                await bot.send_media_group(chat_id=id, media=input_media_photos)
            except:
                await bot.send_message(chat_id=id, text='Фото не получены. Возможно, на сайте видеоматериалы')
            mes = f'<b>{"🔹".join([f" {i} " for i in list_of_prop if i])}</b>\nОписание: {descr[:250] + " ..." if len(descr) > 250 else descr}\n<i>актуально на {data[7]}</i>'
            await bot.send_message(chat_id=id, text=mes,
                                   reply_markup=InlineKeyboards(data[0], data[5]).product_more_buttons(),
                                   disable_web_page_preview=True, parse_mode='HTML')
        except aiogram.exceptions.TelegramForbiddenError:
            print(f'\033[1;31m*** TelegramForbiddenError. USER:{id} ***\033[0m')
        except aiogram.exceptions.TelegramBadRequest:
            print(f'\033[1;31m*** TelegramBadRequest. USER:{id} ***\033[0m')


@dp.message(Command('start'))
async def start_chat(message: Message) -> None:
    user_id = message.chat.id
    try:
        pg_insert_new_user(str(user_id), access_expire=datetime.now() + timedelta(hours=24),
                           username=message.from_user.username)
        await message.answer(text=f'Добро пожаловать, {message.from_user.first_name}!')
        chats_id = pg_select_all_users_id(['users', 'admins', 'superadmins', 'newbies'])  ##
        for chat_id in chats_id:
            await bot.send_message(chat_id=chat_id, text=f'🥳 К боту присоеденился новый пользователь: '
                                                         f'@{message.chat.username}',  # и id: {message.chat.id}',
                                   reply_markup=InlineKeyboards(message.from_user.id, 'newbies').handle_user())
    except IntegrityError:
        await message.answer(text=f'Рады видеть Вас снова, {message.from_user.first_name}!')
        chats_id = pg_select_all_users_id(['users', 'admins', 'superadmins', 'newbies'])
        for chat_id in chats_id:
            await bot.send_message(chat_id=chat_id, text=f'🥳 К боту присоеденился новый пользователь '
                                                         f'{message.from_user.first_name}, с ником: '
                                                         f'@{message.chat.username}',  # и id: {message.chat.id}',
                                   reply_markup=InlineKeyboards(param1=message.from_user.id, param2='newbies',
                                                                param3='day')
                                   .handle_user())


@dp.callback_query(UserCallbackData.filter())
async def user_to_users(callback: CallbackQuery, callback_data: UserCallbackData):
    pg_change_user_group(callback_data.user_id, callback_data.group)
    period_ = datetime.now()
    if callback_data.period == 'week':
        period_ += timedelta(weeks=1)
    elif callback_data.period == '1month':
        period_ += timedelta(days=30)
    elif callback_data.period == '3month':
        period_ += timedelta(days=90)
    elif callback_data.period == 'forever':
        period_ = None
    else:
        pass
    pg_change_user_access_period(callback_data.user_id, period=period_)
    try:
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboards(param1=callback_data.user_id, param2=callback_data.group,
                                         param3=callback_data.period).handle_user()
        )
    except aiogram.exceptions.TelegramBadRequest:
        pass
