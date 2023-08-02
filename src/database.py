from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import INT, Column
from sqlalchemy import create_engine
from src.types.settings import Settings, DATABASE_URL


class Base(DeclarativeBase):
    engine = create_engine(DATABASE_URL)
    session = sessionmaker(bind=engine)

    id = Column(INT, primary_key=True)
