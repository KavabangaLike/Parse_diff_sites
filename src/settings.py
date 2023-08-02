from pathlib import Path
from aiogram import Bot, Dispatcher
# from aiogram.types import BotCommand, BotCommandScope, BotCommandScopeAllPrivateChats
# from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums.parse_mode import ParseMode
# from src.types.settings import Settings

BASE_DIR = Path(__file__).resolve().parent.parent
# SETTINGS = Settings()

bot = Bot(
    token='6306659052:AAE_CO07WXocfidvniOKJ4HloTzjaYA0QzU',
    parse_mode=ParseMode.HTML
)

dp = Dispatcher()

