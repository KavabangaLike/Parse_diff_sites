from sqlalchemy import Column, VARCHAR, BOOLEAN, INT, ForeignKey, TEXT, SMALLINT, FLOAT, TIMESTAMP, BIGINT
from sqlalchemy.orm import relationship
from src.database import Base


class Product(Base):
    __tablename__ = 'product'
    product_id = Column(BIGINT, unique=True, nullable=False)
    product_link = Column(VARCHAR(512), unique=True, nullable=False)
    title = Column(VARCHAR(256), nullable=False)
    land = Column(INT, ForeignKey('land.id', ondelete='RESTRICT'))  # NEW how to add nullable=False?
    price = Column(FLOAT)
    currency = Column(INT, ForeignKey('currency.id', ondelete='RESTRICT'), nullable=False)
    in_month = Column(BOOLEAN, default=True)
    facilities = relationship('ProductFacility', backref='Product')
    description = Column(TEXT)
    profile_url = Column(VARCHAR(512))
    pictures = relationship('Picture', backref='Product')
    expose_datetime = Column(TIMESTAMP, nullable=False)
    status = Column(SMALLINT, default=1, nullable=False)


class Facility(Base):  # Удобства
    __tablename__ = 'facility'
    name = Column(VARCHAR(256), nullable=False, unique=True)
    type = Column(SMALLINT, nullable=False)  # удобство или тип недвижимости или количество комнат
    user_facility = relationship('UserFacility', backref='Facility')


class ProductFacility(Base):  # удобства, которые есть в объявлении
    __tablename__ = 'product_facility'

    product_id = Column(INT, ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    facility_id = Column(INT, ForeignKey('facility.id', ondelete='CASCADE'), nullable=False)


class Keyword(Base):  # ключевые слова для фильтрации удобств
    __tablename__ = 'keyword'
    name = Column(VARCHAR(256), nullable=False)
    facility_id = Column(INT, ForeignKey('facility.id', ondelete='CASCADE'), nullable=False)


class Picture(Base):
    __tablename__ = 'picture'
    link = Column(VARCHAR(512), nullable=False)
    product_id = Column(INT, ForeignKey('product.id', ondelete='CASCADE'), nullable=False)


class Currency(Base):  # Валюта
    __tablename__ = 'currency'
    symbol = Column(VARCHAR(32))


class TgUser(Base):   # !!!!!!!!!!!!!!!!!!!!!!!!
    __tablename__ = 'tg_user'
    id = Column(BIGINT, unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(64), nullable=True)
    access_expire = Column(TIMESTAMP, nullable=True)  #заканчиваться доступ к объявлениям
    show_products = Column(BOOLEAN, default=True)  # показывать объявления (кнопка стоп)
    user_group_id = Column(INT, ForeignKey('user_group.id', ondelete='RESTRICT'), nullable=False)


class UserLand(Base):  # Показ только объявлений на определенной территории
    __tablename__ = 'user_land'
    user_id = Column(BIGINT, ForeignKey('tg_user.id', ondelete='CASCADE'), nullable=False)  # ЕСЛИ УДАЛЕНИЕ, ТО ЧТО БУДЕТ С ПРОГРАММОЙ??
    land_id = Column(INT, ForeignKey('land.id', ondelete='CASCADE'), nullable=False)


class UserFacility(Base):  # Показ только объявлений с определенными удобствами
    __tablename__ = 'user_facility'
    user_id = Column(BIGINT, ForeignKey('tg_user.id', ondelete='CASCADE'), nullable=False)  # ЕСЛИ УДАЛЕНИЕ, ТО ЧТО БУДЕТ С ПРОГРАММОЙ??
    facility_id = Column(INT, ForeignKey('facility.id', ondelete='CASCADE'), nullable=False)  # дублирующиеся связи в many-to-many


class UserGroup(Base):
    __tablename__ = 'user_group'
    name = Column(VARCHAR(64), nullable=False, unique=True, default='newbies')
    users = relationship('TgUser', backref='UserGroup')


class FbUser(Base):  # facebook пользователи для авторизации
    __tablename__ = 'fb_user'
    login = Column(VARCHAR(128), unique=True, nullable=False)
    password = Column(VARCHAR(128), nullable=False)


class Land(Base):
    __tablename__ = 'land'
    name = Column(VARCHAR(128), unique=True, nullable=False)
    link_name = Column(VARCHAR(128), nullable=False, unique=True)
    links = relationship('SearchLink', backref='Land')
    product = relationship('Product', backref='Land')


class SearchLink(Base):  # ссылки для поиска объявлений
    __tablename__ = 'search_link'
    link = Column(VARCHAR(512), unique=True, nullable=False)
    land_id = Column(BIGINT, ForeignKey('land.id', ondelete='NO ACTION'), nullable=False)
    query = Column(VARCHAR(128))


class UserLink(Base):       # ?????????????????????????????????????????
    __tablename__ = 'user_link'

    user_id = Column(BIGINT, ForeignKey('tg_user.id', ondelete='CASCADE'), nullable=False)
    link_id = Column(INT, ForeignKey('search_link.id', ondelete='CASCADE'), nullable=False)