from src.models import Facility, Keyword
from database import pg_select_facility


def filter_user_facilities(user_id):
    periods = pg_select_facility(1)
