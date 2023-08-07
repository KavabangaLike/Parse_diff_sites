import logging
from src.settings import dp, bot
import asyncio
from src.handlers import handlers

logging.basicConfig(level=logging.INFO)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
