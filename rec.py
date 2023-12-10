import asyncio
import logging

from aiogram.filters import Command
from aiogram.types import Message

from database import pg_select_users
from src.database.models import TgUser, UserGroup
from src.keyboards.inline.ik import InlineKeyboards
from src.settings import dp, bot

logging.basicConfig(level=logging.INFO)


def pg_sel(groups: list[str]) -> list[TgUser]:  #
    users = []
    with TgUser.session() as session:
        query = session.query(TgUser.id, TgUser.min_price, TgUser.max_price, TgUser.username).join(UserGroup) \
            .filter(UserGroup.name.in_(groups))
        users.extend(query.all())
    return users


@dp.message(Command('rec'))
async def show_users(message: Message):
    users = pg_select_users(['superadmins'])
    for user in users:
        us = pg_sel(['newbies'])
        for u in us:
            await bot.send_message(chat_id=user.id, text=f'#new_user '
                                                         f'Пользователь, с ником: '
                                                         f'@{u.username} и id: {u.id}',
                                   reply_markup=InlineKeyboards(param1=u.id, param2='newbies',
                                                                param3='day')
                                   .handle_user())

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())