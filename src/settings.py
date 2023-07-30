from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScope, BotCommandScopeAllPrivateChats
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums.parse_mode import ParseMode
from ujson import loads, dumps
from celery import Celery

from .types import Settings

BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS = Settings()

bot = Bot(
    token=SETTINGS.BOT_TOKEN.get_secret_value(),
    session=AiohttpSession(json_loads=loads, json_dumps=dumps),
    parse_mode=ParseMode.HTML
)


dp = Dispatcher(disable_fsm=True)

URLS = (
    ('/filter?sort=4', 'https://cars.av.by'),
    ('/filter?page=2&sort=4', 'https://cars.av.by'),
    ('/filter?sort=4', 'https://truck.av.by'),
    ('/filter?sort=4', 'https://moto.av.by'),
    ('/filter?page=2&sort=4', 'https://moto.av.by'),
    ('/filter?sort=4', 'https://bus.av.by'),
)

celery = Celery()
celery.config_from_object(SETTINGS, namespace='CELERY')  # Ищет необходимые ему аттрибуты в объхекте settings которые начинаются с CELERY
celery.autodiscover_tasks(packages=['src'])


celery.conf.beat_schedule = {
    'parser': {
        'task': 'src.tasks.task_parser',
        'schedule': 1800
    }
}
