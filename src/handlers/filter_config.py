from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from src.keyboards.inline import ik
from database import pg_show_ads, pg_select_lands, pg_select_related_lands, pg_del_related_lands, \
    pg_insert_related_lands, pg_update_user_price, pg_select_facilities, pg_del_related_rooms, pg_insert_related_rooms
from src.keyboards.inline.ik import UserFilterCallbackData
from src.settings import bot
from aiogram.exceptions import TelegramBadRequest

router = Router()


class FilterConfig(StatesGroup):
    choosing_lands = State()
    set_rooms = State()
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


# @router.message(FilterConfig.choosing_lands)
@router.callback_query(UserFilterCallbackData.filter(), FilterConfig.choosing_lands)
async def handle_land_filter(callback: CallbackQuery, callback_data: UserFilterCallbackData, state: FSMContext) -> None:
    data = await state.get_data()
    if callback_data.filter_name in data['user_lands']:
        data['user_lands'].pop(data['user_lands'].index(callback_data.filter_name))
    else:
        data['user_lands'].append(callback_data.filter_name)
    await state.update_data(data)
    await callback.message.edit_reply_markup(
        reply_markup=ik.InlineKeyboards(data['all_lands'], data['user_lands']).user_filter())


# @router.message(FilterConfig.choosing_lands)
@router.callback_query(F.data == "ready_filter", FilterConfig.choosing_lands)
async def show_rooms_filter(callback: CallbackQuery, state: FSMContext) -> None:
    all_rooms = pg_select_facilities(type_=1)
    user_rooms = pg_select_facilities(type_=1, user_id=callback.message.chat.id)
    await callback.message.edit_text(text="Выберите количество комнат:")
    await callback.message.edit_reply_markup(
        reply_markup=ik.InlineKeyboards(param1=all_rooms, param2=user_rooms).user_filter()
    )
    await state.set_state(FilterConfig.set_rooms)
    await state.update_data({"user_rooms": user_rooms, "all_rooms": all_rooms})


# @router.message(FilterConfig.set_rooms)
@router.callback_query(UserFilterCallbackData.filter(), FilterConfig.set_rooms)
async def handle_rooms_filter(callback: CallbackQuery, callback_data: UserFilterCallbackData, state: FSMContext) -> None:
    data = await state.get_data()
    if callback_data.filter_name in data["user_rooms"]:
        data["user_rooms"].pop(data['user_rooms'].index(callback_data.filter_name))
    else:
        data['user_rooms'].append(callback_data.filter_name)
    await state.update_data(data)
    await callback.message.edit_reply_markup(
        reply_markup=ik.InlineKeyboards(data['all_rooms'], data['user_rooms']).user_filter())


# @router.message(FilterConfig.set_rooms)
@router.callback_query(F.data == 'ready_filter', FilterConfig.set_rooms)
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
        if not data.get('user_lands'):
            data['user_lands'] = data['all_lands']
        await state.set_data(data)

        await message.answer(
            text=f'Выбраны следующие параметры:\nЛокации: <i>{" , ".join(data["user_lands"])}</i>\nКоличество комнат: '
                 f'{" , ".join(data["user_rooms"])}\n'
                 f'Цена: {data["min_price"]} - {data["max_price"]} rp',
            reply_markup=ik.InlineKeyboards.save_filter_config())


# @router.message(FilterConfig.save_data)
@router.callback_query(F.data == 'save_config', FilterConfig.save_data)
async def save_filter_config(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    pg_update_user_price(price_type='min_price', price_value=data['min_price'], user_id=callback.message.chat.id)
    pg_update_user_price(price_type='max_price', price_value=data['max_price'], user_id=callback.message.chat.id)
    pg_del_related_lands(user_id=callback.message.chat.id)
    pg_insert_related_lands(user_id=callback.message.chat.id, lands=data['user_lands'])
    pg_del_related_rooms(user_id=callback.message.chat.id)
    pg_insert_related_rooms(user_id=callback.message.chat.id, facilities=data["user_rooms"])
    await callback.message.edit_text(text=f'Сохранен фильтр:\nЛокации: <i>{" , ".join(data["user_lands"])}</i>\nКоличество комнат: '
                                          f'{" , ".join(data["user_rooms"])}\n'
                                          f'Цена: {data["min_price"]}-{data["max_price"]} rp')
    await state.clear()
    pg_show_ads(callback.message.chat.id, True)


