from pathlib import Path
from aiogram import Bot, Dispatcher
# from aiogram.types import BotCommand, BotCommandScope, BotCommandScopeAllPrivateChats
# from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums.parse_mode import ParseMode
from src.types.settings import TOKEN

BASE_DIR = Path(__file__).resolve().parent.parent
# SETTINGS = Settings()

bot = Bot(
    token=TOKEN,
    parse_mode=ParseMode.HTML,
)

dp = Dispatcher()

