from pathlib import Path
from aiogram import Bot, Dispatcher
# from aiogram.types import BotCommand, BotCommandScope, BotCommandScopeAllPrivateChats
# from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.validation.settings import settings

BASE_DIR = Path(__file__).resolve().parent.parent


bot = Bot(
    token=settings.BOT_TOKEN.get_secret_value(),
    parse_mode=ParseMode.HTML,
)

dp = Dispatcher(storage=MemoryStorage())

