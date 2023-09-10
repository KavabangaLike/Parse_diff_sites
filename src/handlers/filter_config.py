import aiogram
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from src.keyboards.inline import ik
from database import pg_show_ads, pg_select_facility, pg_select_related_facility, pg_insert_related_facility, \
    pg_delete_related_facility, pg_select_lands, pg_select_related_lands, pg_del_related_lands, pg_insert_related_lands
from src.keyboards.inline.ik import UserFilterCallbackData, InlineKeyboards

router = Router()


class FilterConfig(StatesGroup):
    choosing_lands = State()


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
@router.callback_query(F.data == 'filter_preview')
async def preview_filter_config(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    if not data['user_lands']:
        data['user_lands'] = data['all_lands']
    await state.set_data(data)

    await callback.message.edit_text(text=f'Выбраны следующие параметры:\nЛокации: {" , ".join(data["user_lands"])}',
                                     reply_markup=ik.InlineKeyboards.save_filter_config())


@router.message(FilterConfig.choosing_lands)
@router.callback_query(F.data == 'save_config')
async def save_filter_config(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    pg_del_related_lands(user_id=callback.message.chat.id)
    pg_insert_related_lands(user_id=callback.message.chat.id, lands=data['user_lands'])
    await callback.message.edit_text(text=f'Сохранен фильтр:\nЛокации: {" , ".join(data["user_lands"])}')
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
