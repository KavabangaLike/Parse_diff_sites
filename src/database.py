from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import INT, Column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import insert, select, create_engine
from src.settings import SETTINGS


class Base(DeclarativeBase):
    engine = create_async_engine(SETTINGS.DATABASE_ASYNC_URL)
    session = async_sessionmaker(bind=engine)

    id = Column(INT, primary_key=True)
