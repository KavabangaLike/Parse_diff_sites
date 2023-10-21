from sqladmin import ModelView
from fastapi import Request
from sqladmin.authentication import AuthenticationBackend

from src.database.models import Product, TgUser, SearchLink


class ProductAdmin(ModelView, model=Product):
    pass


class TgUserAdmin(ModelView, model=TgUser):
    pass


class SLinkAdmin(ModelView, model=SearchLink):
    pass


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


