import aiogram.exceptions
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from aiogram.types.input_media_photo import InputMediaPhoto
from src.settings import bot, dp
from database import pg_insert_new_user, pg_select_all_users_id, pg_change_user_group
from src.keyboards.inline.ik import InlineKeyboards, UserGroupCallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram import F


async def send_all(data: list[str]) -> None:
    photos = data[6].split(',')[:10]
    input_media_photos = [InputMediaPhoto(media=url) for url in photos]
    users_id = pg_select_all_users_id(['users', 'admins', 'superadmins'])
    list_of_prop = [data[2]]
    list_of_prop.extend(data[3].split(','))
    # try:
    #     descr = data[4].encode('latin1').decode('unicode-escape').encode('latin1').decode('utf8').replace('\\/', ' ')
    descr = data[4].replace('\\n', ' ').replace('\\/', '/')
    # except:r
    #     descr = data[4].replace('\\/', ' ').replace('\\n', ' ')
    for id in users_id:
        try:
            try:
                await bot.send_media_group(chat_id=id, media=input_media_photos)
            except:
                await bot.send_message(chat_id=id, text='Фото не получены. Возможно, на сайте видеоматериалы')
            mes = f'<b>{"🔹".join([f" {i} " for i in list_of_prop if i])}</b>\nОписание: {descr[:250] + " ..." if len(descr) > 250 else descr}\n<i>актуально на {data[7]}</i>'
            await bot.send_message(chat_id=id, text=mes, reply_markup=InlineKeyboards(data[0], data[5]).product_more_buttons(),
                             disable_web_page_preview=True, parse_mode='HTML')
        except aiogram.exceptions.TelegramForbiddenError:
            print(f'\033[1;31m*** TelegramForbiddenError. USER:{id} ***\033[0m')
        except aiogram.exceptions.TelegramBadRequest:
            print(f'\033[1;31m*** TelegramBadRequest. USER:{id} ***\033[0m')


@dp.message(Command('start'))
async def start_chat(message: Message) -> None:
    user_id = message.chat.id
    try:
        pg_insert_new_user(str(user_id))
        await message.answer(text=f'Добро пожаловать, {message.from_user.first_name}!')
        chats_id = pg_select_all_users_id(['superadmins'])
        for chat_id in chats_id:
            await bot.send_message(chat_id=chat_id, text=f'🥳 К боту присоеденился новый пользователь: '
                                                         f'@{message.chat.username} и id: {message.chat.id}',
                                   reply_markup=InlineKeyboards(message.from_user.id, 'newbies').handle_user())
    except IntegrityError:
        await message.answer(text=f'Рады видеть Вас снова, {message.from_user.first_name}!')
        chats_id = pg_select_all_users_id(['superadmins'])
        for chat_id in chats_id:
            await bot.send_message(chat_id=chat_id, text=f'🥳 К боту присоеденился новый пользователь '
                                                         f'{message.from_user.first_name}, с ником: '
                                                         f'@{message.chat.username} и id: {message.chat.id}',
                                   reply_markup=InlineKeyboards(param1=message.from_user.id, param2='newbies')
                                   .handle_user())


@dp.callback_query(UserGroupCallbackData.filter())
async def user_to_users(callback: CallbackQuery, callback_data: UserGroupCallbackData):
    pg_change_user_group(callback_data.user_id, callback_data.group)
    await callback.message.edit_reply_markup(
        reply_markup=InlineKeyboards(param1=callback_data.user_id, param2=callback_data.group).handle_user()
    )

