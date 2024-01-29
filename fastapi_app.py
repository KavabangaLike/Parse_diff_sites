from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from src.database.base import Base
from src.database.sql_admin import AdminAuth, ProductAdmin, SLinkAdmin, TgUserAdmin, LandAdmin, UGroupAdmin, \
    KeywordAdmin, FacilityAdmin, UserFacilityAdmin, BProductAdmin

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
admin.add_view(BProductAdmin)



