from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import INT, Column
from sqlalchemy import create_engine
from src.validation.settings import settings


class Base(DeclarativeBase):
    engine = create_engine(settings.DATABASE_URL.unicode_string())
    session = sessionmaker(bind=engine)

    id = Column(INT, primary_key=True)
