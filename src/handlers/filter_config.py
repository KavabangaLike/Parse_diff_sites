import aiogram
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from src.keyboards.inline import ik
from database import pg_show_ads, pg_select_lands, pg_select_related_lands, pg_del_related_lands, \
    pg_insert_related_lands, pg_update_user_price
from src.keyboards.inline.ik import UserFilterCallbackData, InlineKeyboards
from src.models import TgUser
from sqlalchemy import insert
from src.settings import bot
from aiogram.exceptions import TelegramBadRequest

router = Router()


class FilterConfig(StatesGroup):
    choosing_lands = State()
    set_min_price = State()
    set_max_price = State()
    save_data = State()


@router.message(Command("tune"))
async def cmd_tune(message: Message, state: FSMContext) -> None:
    pg_show_ads(message.from_user.id, False)
    all_lands = pg_select_lands()
    user_lands = pg_select_related_lands(user_id=message.from_user.id)
    await message.answer(
        text="Выберите локации:",
        reply_markup=ik.InlineKeyboards(param1=all_lands, param2=user_lands).user_filter()
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(FilterConfig.choosing_lands)
    await state.set_data({'user_lands': user_lands, 'all_lands': all_lands})

    # d = await state.get_data()
    # print(d)


@router.message(FilterConfig.choosing_lands)
@router.callback_query(UserFilterCallbackData.filter())
async def handle_land_filter(callback: CallbackQuery, callback_data: UserFilterCallbackData, state: FSMContext) -> None:
    data = await state.get_data()
    if callback_data.filter_name in data['user_lands']:
        data['user_lands'].pop(data['user_lands'].index(callback_data.filter_name))
    else:
        data['user_lands'].append(callback_data.filter_name)
    await state.update_data(data)
    await callback.message.edit_reply_markup(
        reply_markup=ik.InlineKeyboards(data['all_lands'], data['user_lands']).user_filter())


@router.message(FilterConfig.choosing_lands)
@router.callback_query(F.data == 'ready_land_filter')
async def min_price_config(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FilterConfig.set_min_price)
    await callback.message.edit_text(text='Введите <b>минимальную</b> цену в rp:')
    await state.update_data({'last_message_id': callback.message.message_id})


async def delete_last_messages(message: Message, state: FSMContext):
    try:
        await bot.delete_message(message.chat.id, (d := await state.get_data())['last_message_id'])
        await bot.delete_message(message.chat.id, message.message_id)
    except TelegramBadRequest:
        pass


@router.message(FilterConfig.set_min_price)
async def handle_price(message: Message, state: FSMContext):
    min_price = message.text.strip()
    try:
        min_price = int(min_price)
    except ValueError:
        await delete_last_messages(message, state)
        await state.update_data({'last_message_id': (m := await message.answer(
            text='❗️ Введите корректное целочисленное значение <b>минимальной</b> цены, например: 10:')).message_id})
    else:
        await state.update_data({'min_price': min_price})
        await state.set_state(FilterConfig.set_max_price)

        await delete_last_messages(message, state)
        await state.update_data({'last_message_id': (m := await message.answer(
            text='Введите максимальную цену в rp:')).message_id})


@router.message(FilterConfig.set_max_price)
async def handle_price(message: Message, state: FSMContext):
    max_price = message.text.strip()
    try:
        max_price = int(max_price)
    except ValueError:
        await delete_last_messages(message, state)
        await state.update_data({'last_message_id': (m := await message.answer(
            text='❗️ Введите корректное целочисленное значение <b>максимальной</b> цены, например: 5000000:')).message_id})
    else:
        if max_price <= (d := await state.get_data())['min_price']:
            print((d := await state.get_data())['min_price'])
            await state.set_state(FilterConfig.set_min_price)
            await delete_last_messages(message, state)
            await state.update_data({'last_message_id': (m := await message.answer(
                text='❗️ Некорректные границы цен. Пожалуйста, введите <b>минимальную</b> цену:')).message_id})
            return

        await state.update_data({'max_price': max_price})
        await delete_last_messages(message, state)

        await state.set_state(FilterConfig.save_data)
        data = await state.get_data()
        if not data['user_lands']:
            data['user_lands'] = data['all_lands']
        await state.set_data(data)

        await message.answer(
            text=f'Выбраны следующие параметры:\nЛокации: <i>{" , ".join(data["user_lands"])}</i>\n'
                 f'Цена: {data["min_price"]} - {data["max_price"]} rp',
            reply_markup=ik.InlineKeyboards.save_filter_config())


@router.message(FilterConfig.save_data)
@router.callback_query(F.data == 'save_config')
async def save_filter_config(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    pg_update_user_price(price_type='min_price', price_value=data['min_price'], user_id=callback.message.chat.id)
    pg_update_user_price(price_type='max_price', price_value=data['max_price'], user_id=callback.message.chat.id)
    pg_del_related_lands(user_id=callback.message.chat.id)
    pg_insert_related_lands(user_id=callback.message.chat.id, lands=data['user_lands'])
    await callback.message.edit_text(text=f'Сохранен фильтр:\nЛокации: <i>{" , ".join(data["user_lands"])}</i>\n'
                                          f'Цена: {data["min_price"]}-{data["max_price"]} rp')
    await state.clear()
    pg_show_ads(callback.message.chat.id, True)

# @router.message(Command('tune'))
# async def set_product_filter(message: Message):
#     pg_show_ads(message.from_user.id, False)
#     all_lands = pg_select_lands()
#     user_lands = pg_select_related_lands(user_id=message.from_user.id)
#     print(1111, user_lands)
#     await message.answer(text='Выберите период аренды:', reply_markup=InlineKeyboards(all_lands, user_lands, message.from_user.id, 1).user_filter())
#
# @router.callback_query(UserFilterCallbackData.filter(F.type_ == 1))
# async def filter_period_for_rent(callback: CallbackQuery, callback_data: UserFilterCallbackData):
#     pg_insert_related_facility(callback_data.user_id, [callback_data.filter_name])
#     all_periods = pg_select_facility(1)
#     user_periods = pg_select_related_facility(callback_data.user_id, 1)
#     try:
#         await callback.message.edit_reply_markup(
#             reply_markup=InlineKeyboards(param1=all_periods, param2=user_periods,
#                                          param3=callback_data.user_id, param4=callback_data.type_).user_filter()
#         )
#     except aiogram.exceptions.TelegramBadRequest:
#         pg_delete_related_facility(callback_data.user_id, callback_data.filter_name)
#         user_periods = pg_select_related_facility(callback_data.user_id, 1)
#         await callback.message.edit_reply_markup(
#             reply_markup=InlineKeyboards(param1=all_periods, param2=user_periods,
#                                          param3=callback_data.user_id, param4=callback_data.type_).user_filter()
#         )
#
