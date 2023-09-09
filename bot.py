import logging
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from src.settings import dp, bot
import asyncio
from src.handlers import handlers

logging.basicConfig(level=logging.INFO)


async def on_startup():
    await bot.set_my_commands(
        commands=[
            # BotCommand(command='/tune', description='🎛  Configure the Ad filter'),
            BotCommand(command='/pause', description='⏸  Suspend the search for new ads'),
            BotCommand(command='/start', description='▶️  Start searching for housing in Bali!')
        ],
        scope=BotCommandScopeAllPrivateChats(),
        language_code='en'
    )
    await bot.set_my_commands(
        commands=[
            # BotCommand(command='/tune', description='🎛  Настроить фильтр объявлений'),
            BotCommand(command='/pause', description='⏸  Приостановить поиск новых объявлений'),
            BotCommand(command='/start', description='▶️  Начать поиск жилья на Бали!')
        ],
        scope=BotCommandScopeAllPrivateChats(),
        language_code='ru'
    )


async def main():
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
