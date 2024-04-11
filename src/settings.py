from pathlib import Path
from aiogram import Bot, Dispatcher
# from aiogram.types import BotCommand, BotCommandScope, BotCommandScopeAllPrivateChats
# from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from celery import Celery
from src.validation.settings import settings

BASE_DIR = Path(__file__).resolve().parent.parent
DELAY_LIMITER = 300

bot = Bot(
    token=settings.BOT_TOKEN.get_secret_value(),
    parse_mode=ParseMode.HTML,
)

dp = Dispatcher(storage=MemoryStorage())

celery = Celery()
celery.config_from_object(settings, namespace='CELERY')  # Ищет необходимые ему аттрибуты в объхекте settings которые начинаются с CELERY
celery.autodiscover_tasks(packages=['src'])


celery.conf.beat_schedule = {
    'fb_parser': {
        'task': 'src.tasks.start_fb_parse',
        'schedule': DELAY_LIMITER * 7
    },
    'baliving_parser': {
        'task': 'src.tasks.start_baliving_parse',
        'schedule': DELAY_LIMITER
    }
}

