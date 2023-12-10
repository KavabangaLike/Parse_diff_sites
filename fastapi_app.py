from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
from sqlalchemy import or_

from src.database.models import UserGroup
from src.database.sql_admin import AdminAuth, ProductAdmin, SLinkAdmin, TgUserAdmin, LandAdmin, UGroupAdmin,\
    KeywordAdmin, FacilityAdmin, UserFacilityAdmin
from src.database.base import Base

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   **{'allow_methods': ('*',), 'allow_origins': ('*',),
                      'allow_headers': ('*',), 'allow_credentials': True})

sqladmin_auth_backend = AdminAuth(secret_key="...")
admin = Admin(app=app, authentication_backend=sqladmin_auth_backend, engine=Base.engine)
admin.add_view(ProductAdmin)
admin.add_view(TgUserAdmin)
admin.add_view(SLinkAdmin)
admin.add_view(LandAdmin)
admin.add_view(UGroupAdmin)
admin.add_view(FacilityAdmin)
admin.add_view(KeywordAdmin)
admin.add_view(UserFacilityAdmin)



