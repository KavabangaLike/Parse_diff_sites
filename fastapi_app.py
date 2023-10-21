from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
from src.database.sql_admin import AdminAuth, ProductAdmin, SLinkAdmin, TgUserAdmin

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   **{'allow_methods': ('*',), 'allow_origins': ('*',),
                      'allow_headers': ('*',), 'allow_credentials': True})

ab = AdminAuth(secret_key="...")
admin = Admin(app=app, authentication_backend=ab)
admin.add_view(ProductAdmin)
admin.add_view(TgUserAdmin)
admin.add_view(SLinkAdmin)
