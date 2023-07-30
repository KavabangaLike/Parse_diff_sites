from sqlalchemy import Column, VARCHAR, BOOLEAN, INT, ForeignKey, BIGINT, TEXT

from src.database import Base


class Products(Base):
    __tablename__ = 'products'
    product_link = Column(VARCHAR(256), unique=True)
    title = Column(VARCHAR(256))
    price = Column(VARCHAR(128))
    area = Column(VARCHAR(64))
    product_type = Column(VARCHAR(64))
    rooms = Column(VARCHAR(64))
    description = Column(TEXT)
    pictures = Column(TEXT)
    current = Column(VARCHAR(64))
