from sqladmin import ModelView
from fastapi import Request
from sqladmin.authentication import AuthenticationBackend

from src.database.models import Product, TgUser, SearchLink, Land, UserGroup, Facility, UserFacility, Keyword


class ProductAdmin(ModelView, model=Product):
    column_list = ["land_", "title", "price", "curr"]
    column_default_sort = [(Product.expose_datetime, True)]
    name = "Объявление"
    name_plural = "Объявления"
    category = "Веб-скрапинг"


class TgUserAdmin(ModelView, model=TgUser):
    column_list = ["id", "username", "access_expire", "min_price", "max_price", "user_group_id"]
    name = "Пользователь"
    name_plural = "Пользователи"
    can_create = False
    can_edit = True
    can_delete = False
    category = "Аккаунты"


class SLinkAdmin(ModelView, model=SearchLink):
    column_list = ["link", "land_id"]
    name = "Ссылка"
    name_plural = "Ссылки для парсинга"
    can_delete = False
    can_edit = True
    can_create = False
    category = "Веб-скрапинг"


class LandAdmin(ModelView, model=Land):
    column_list = ["id", "name"]
    name = "Локация"
    name_plural = "Локации"
    can_edit = False
    can_delete = False
    can_create = False
    category = "Веб-скрапинг"


class UGroupAdmin(ModelView, model=UserGroup):
    column_list = ["id", "name", "users"]
    name = "Группа"
    name_plural = "Группы"
    can_create = False
    can_edit = False
    can_delete = False
    category = "Аккаунты"


class FacilityAdmin(ModelView, model=Facility):
    column_list = ["id", "name", "keywords"]
    name = "Удобство"
    name_plural = "Удобства"
    can_create = True
    can_edit = False
    can_delete = False
    category = "Веб-скрапинг"


class KeywordAdmin(ModelView, model=Keyword):
    column_list = ["name", "facility"]
    name = "Ключевое слово"
    name_plural = "Ключевые слова"
    can_delete = True
    can_edit = True
    can_create = True
    category = "Веб-скрапинг"


class UserFacilityAdmin(ModelView, model=UserFacility):
    column_list = ["name", "facility"]
    name = "R"
    name_plural = "Rs"
    can_delete = True
    can_edit = True
    can_create = True
    category = "Веб-скрапинг"


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        valid_usernames = ["admin", "root"]
        valid_passwords = ["fb_Admin", "Cloudy2c"]
        # Validate username/password credentials
        # And update session
        request.session.update({"token": "..."})
        if username in valid_usernames and password in valid_passwords:
            return True
        return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


