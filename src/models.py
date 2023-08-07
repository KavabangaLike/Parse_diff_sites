from sqlalchemy import Column, VARCHAR, BOOLEAN, INT, ForeignKey, TEXT, SMALLINT
from sqlalchemy.orm import relationship
from src.database import Base


class Products(Base):
    __tablename__ = 'products'
    product_id = Column(VARCHAR(128))
    product_link = Column(VARCHAR(512), unique=True)
    title = Column(VARCHAR(256))
    price = Column(VARCHAR(128))
    product_prop = Column(VARCHAR(256))
    description = Column(TEXT)
    pictures = Column(TEXT)
    profile_url = Column(VARCHAR(512))
    current = Column(VARCHAR(64))
    is_active = Column(SMALLINT, default=1)


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(VARCHAR(128))
    group = Column(VARCHAR(64))
    searching_links_id = Column(INT, ForeignKey('searching_links.id'))


class FbUsers(Base):
    __tablename__ = 'fb_users'
    login = Column(VARCHAR(128), unique=True)
    password = Column(VARCHAR(128))


class SearchingLinks(Base):
    __tablename__ = 'searching_links'
    link = Column(VARCHAR(512), unique=True)
    geo = Column(VARCHAR(256))
    query = Column(VARCHAR(256))