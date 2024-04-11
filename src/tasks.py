from src.utils.baliving import BalivingScraper
from src.app import parsing
from .settings import celery


@celery.task
def start_fb_parse() -> None:
    parsing()


@celery.task
def start_baliving_parse() -> None:
    BalivingScraper().handle_data()
