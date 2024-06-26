from datetime import datetime, timedelta

import aiogram.exceptions
from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_media_photo import InputMediaPhoto
from sqlalchemy import select, or_

from src.database import pg_insert_new_user, pg_select_users, pg_change_user_group, pg_change_user_access_period, \
    pg_show_ads
from src.database.models import Facility, TgUser, UserGroup
from src.keyboards.inline.ik import InlineKeyboards, UserCallbackData
from src.settings import bot

router = Router()


async def send_all(data: list[str | datetime | float]) -> None:
    photos = data[6].split(',')[:10]
    input_media_photos = [InputMediaPhoto(media=url) for url in photos]
    list_of_prop = [data[8]]
    list_of_prop.extend(data[3].split(','))
    # descr = data[4].replace('\\n', ' ').replace('\\/', '/').strip("'")
    descr = data[1]
    digit_price = data[2]
    list_of_prop, price = '', data[8]
    geo, land = data[-1], data[-1].split('(')[1].replace(')', '').strip()


    users = pg_select_users(['users', 'admins', 'superadmins', 'newbies'])

    product_facilities = []
    find_descr = descr.lower()
    with Facility.session() as session:
        facilities_ = session.scalars(select(Facility)).all()
        for facility_ in facilities_:
            for keyword_ in facility_.keywords:
                if keyword_.name in find_descr:
                    product_facilities.append(facility_.id)


    # users_land_filter = pg_select_userland_user(land=land)
    filtered_users = []
    users = []
    with TgUser.session() as session:
        query = session.query(TgUser).join(UserGroup) \
            .filter(UserGroup.name.in_(['users', 'admins', 'superadmins', 'newbies'])) \
            .filter(or_(datetime.now() < TgUser.access_expire, TgUser.access_expire == None)) \
            .filter(TgUser.show_products == True)
        users.extend(query.all())

        for user in users:
            users_land_filter = {ul.land for ul in user.user_land}
            user_facility_filter = {uf.facility for uf in user.user_facility}
            if user.max_price and (land in users_land_filter) and \
                    ([f.id in product_facilities for f in user_facility_filter] or user_facility_filter is None):
                if user.min_price <= digit_price <= user.max_price:
                    filtered_users.append(user)
            elif user.id in users_land_filter:
                filtered_users.append(user)

    for user in filtered_users:
        try:
            try:
                await bot.send_media_group(chat_id=user.id, media=input_media_photos)
            except:
                await bot.send_message(chat_id=user.id, text='Фото не получены. Возможно, на сайте видеоматериалы')

            mes = f'<b>{"🔹".join([f" {i} " for i in list_of_prop if i])}{price} <i>{geo}</i></b>\n' \
                  f'Описание: {descr[:250] + " ..." if len(descr) > 250 else descr}\n<i>актуально на ' \
                  f'{data[7].strftime("%b %d %Y %H:%M:%S")}</i>'

            await bot.send_message(chat_id=user.id, text=mes,
                                   reply_markup=InlineKeyboards(data[0], data[5]).product_more_buttons(),
                                   disable_web_page_preview=True, parse_mode='HTML')
        except aiogram.exceptions.TelegramForbiddenError:
            print(f'\033[1;31m*** TelegramForbiddenError. USER:{user.id} ***\033[0m')
        except aiogram.exceptions.TelegramBadRequest:
            print(f'\033[1;31m*** TelegramBadRequest. USER:{user.id} ***\033[0m')


@router.message(Command('start'))
async def start_chat(message: Message) -> None:
    groups_to_enter = {"@mr_solar_blog": -1001144316841, "@solar_property": -1002118216226}
    user_id = message.chat.id
    with TgUser.session() as session:
        current_user: TgUser = session.scalar(select(TgUser).filter(TgUser.id == user_id))
        if not current_user:
            pg_insert_new_user(user_id=str(user_id), access_expire=datetime.now() - timedelta(hours=72),
                               username=message.from_user.username)
            await message.answer(text=f'Добро пожаловать, {message.from_user.first_name}! Для доступа проверьте подписки на группы: \n'
                                      f'{", ".join([group_name for group_name in groups_to_enter.keys()])} и нажмите /start.\n'
                                      f' По всем вопросам обращайтесь к @yuriy_solar')

            admins = pg_select_users(['superadmins'])  ##  !!!!!!!!!!!!!!!
            for user in admins:
                await bot.send_message(chat_id=user.id, text=f'#new_user '
                                                             f'{message.from_user.first_name}, с ником: '
                                                             f'@{message.chat.username} и id: {message.chat.id}',
                                       reply_markup=InlineKeyboards(param1=message.from_user.id, param2='newbies',
                                                                    param3='day')
                                       .handle_user())

        elif current_user.group.name == "newbies":
            groups_member = [await bot.get_chat_member(chat_id=group_id, user_id=user_id) for group_id in groups_to_enter.values()]

            if any([group.status == "left" for group in groups_member]):
                await message.answer(text='Для доступа проверьте подписки на группы: \n'
                                      f'{", ".join([group_name for group_name in groups_to_enter.keys()])} и нажмите /start.\n'
                                      f' По всем вопросам обращайтесь к @yuriy_solar')
            else:
                current_user.access_expire = datetime.now() + timedelta(hours=72)
                current_user.user_group_id = select(UserGroup.id).filter(UserGroup.name == "users")
                session.add(current_user)
                session.commit()
                await message.answer(text="На данный момент у Вас 3-ех "
                                     f"дневный доступ к боту. Настройте фильтр объявлений, нажав /tune."
                                     f" Для увеличения периода подписки обращайтесь к @yuriy_solar")
        else:
            pg_show_ads(message.from_user.id, True)
            await message.answer(text=f'Рады видеть Вас снова, {message.from_user.first_name}!')

    # try:
    #     group_ids = ["-4085606102", ]
    #     groups = []
    #     for group_id in group_ids:
    #         member_of_group = await bot.get_chat_member(chat_id=group_id, user_id=user_id)
    #         groups.append(member_of_group)
    #         print(any([group.status == "left" for group in groups]))
    #         print([group.status == "left" for group in groups])
    #     if any([group.status == "left" for group in groups]):
    #         await bot.send_message(text="YEAAAR", chat_id=message.chat.id)
    #     pg_insert_new_user(str(user_id), access_expire=datetime.now() + timedelta(hours=24),
    #                        username=message.from_user.username)
    #     await message.answer(text=f'Добро пожаловать, {message.from_user.first_name}! На данный момент у Вас 3-ех '
    #                               f'дневный доступ к ресурсам нашего бота. По всем вопросам обращайтесь к @yuriy_solar')
    #     users = pg_select_users(['superadmins'])  ##  !!!!!!!!!!!!!!!
    #     for user in users:
    #         await bot.send_message(chat_id=user.id, text=f'#new_user '
    #                                                      f'{message.from_user.first_name}, с ником: '
    #                                                      f'@{message.chat.username} и id: {message.chat.id}',
    #                                reply_markup=InlineKeyboards(param1=message.from_user.id, param2='newbies',
    #                                                             param3='day')
    #                                .handle_user())
    # except IntegrityError:
    #     pg_show_ads(message.from_user.id, True)
    #     await message.answer(text=f'Рады видеть Вас снова, {message.from_user.first_name}!')


@router.callback_query(UserCallbackData.filter())
async def user_to_users(callback: CallbackQuery, callback_data: UserCallbackData):
    pg_change_user_group(callback_data.user_id, callback_data.group)
    period_ = datetime.now()
    if callback_data.period == 'week':
        period_ += timedelta(weeks=1)
    elif callback_data.period == '1month':
        period_ += timedelta(days=30)
    elif callback_data.period == '2month':
        period_ += timedelta(days=60)
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


@router.message(Command('pause'))
async def pause_show_ads(message: Message) -> None:
    pg_show_ads(message.from_user.id, False)
    await message.answer(text='😴 Новые объявления пока что появляться не будут. Для возобновления нажмите /start')


@router.message(Command(commands=["cancel"]))
@router.callback_query(F.data == 'cancel')
async def cmd_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text="Действие отменено."
    )
    pg_show_ads(callback.message.chat.id, True)


@router.message(F.text.contains("#new"))  # Рассылка всем пользователям сообщения
async def newsletter(message: Message):
    with TgUser.session() as session:
        admins_ids = session.scalars(select(TgUser.id).filter(TgUser.user_group_id.in_(select(UserGroup.id).filter(UserGroup.name.in_(("admins", "superadmins"))))))
        if message.from_user.id in admins_ids:
            all_users_ids = session.scalars(select(TgUser.id))
            for id_ in all_users_ids:
                try:
                    await bot.send_message(chat_id=id_, text=message.text.replace("#new", ""))
                except aiogram.exceptions.TelegramBadRequest:
                    continue


@router.message(F.text.contains("UISH&*$*RYFOIUDHRNLGFD"))
async def reset_all(message: Message):
    groups_to_enter = {"@mr_solar_blog": -1001144316841, "@solar_property": -1002118216226}
    with TgUser.session() as session:
        all_users: list[TgUser] = session.scalars(select(TgUser))
        for user in all_users:
            user.user_group_id = select(UserGroup.id).filter(UserGroup.name == "newbies")
            user.access_expire = datetime.now() - timedelta(hours=72)
            session.add(user)  # можно add_all(), но сделаю так на всякий
            session.commit()
            try:
                await bot.send_message(chat_id=user.id, text=f'Доброго времени суток! Для доступа проверьте подписки на группы: \n'
                                      f'{", ".join([group_name for group_name in groups_to_enter.keys()])} и нажмите /start.\n'
                                      f' По всем вопросам обращайтесь к @yuriy_solar')
            except aiogram.exceptions.TelegramForbiddenError:
                continue
 

@router.message(Command("show_users"))
async def show_users_to_superadmins(message: Message):
    with TgUser.session() as session:
        superadmins_ids = session.scalars(select(TgUser.id).filter(TgUser.user_group_id.in_(select(UserGroup.id).filter(UserGroup.name.in_(("superadmins", ))))))
        if message.chat.id in superadmins_ids:
            users = session.scalars(select(TgUser.id).filter(TgUser.user_group_id.in_(select(UserGroup.id).filter(UserGroup.name.in_(("admins", "users", "newbies"))))))

            for superadmin_id in superadmins_ids:
                for user in users:
                    await bot.send_message(chat_id=superadmin_id, text=f'#new_user '
                                                                 f'с ником: '
                                                                 f'@{user.username} и id: {user.id}',
                                           reply_markup=InlineKeyboards(param1=user.id, param2='newbies',
                                                                        param3='day')
                                           .handle_user())
