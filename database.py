import sqlite3
from src.models import Products, Users
from sqlalchemy import select
from src.utils.google_sheet import gh_prepare_data, gh_insert



class DataBase:
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    @classmethod
    def get(cls, item_to_select: str, table: str) -> list[str]:
        sql = f'SELECT {item_to_select} FROM {table}'
        return [url[0] for url in [*cls.cursor.execute(sql)]]

    @classmethod
    def post_product(cls, data: list[str]) -> None:
        sql_insert = 'INSERT INTO products(id, product_link, title, price, product_prop, description, profile_url, pictures, current) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cls.cursor.execute(sql_insert, (data[0].split('/')[5], data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],))
        cls.connection.commit()

    @classmethod
    def add_user(cls, user_id: str) -> None:
        sql_add = 'INSERT INTO users(id) VALUES (?)'
        cls.cursor.execute(sql_add, (user_id, ))
        cls.connection.commit()

    # @classmethod
    # def insert_disable(cls):
    #     sql= 'INSERT INTO products(id) VALUES (?) WHERE product_link'


def pg_insert_product(data):
    with Products.session() as session:
        product = Products(
            product_id=data[0].split('/')[5],
            product_link=data[0],
            title = data[1],
            price = data[2],
            product_prop = data[3],
            description = data[4],
            profile_url = data[5],
            pictures=data[6],
            current = data[7],
        )
        session.add(product)
        session.commit()
        session.refresh(product)


def pg_select_product_links():
    with Products.session() as session:
        query = select(Products.product_id)
        result = session.execute(query)
        return [i[0] for i in [*result]]


def pg_select_products(low: int, high: int):
    with Products.session() as session:
        query = select(Products.id,
                       Products.product_id,
                       Products.product_link,
                       Products.price,
                       Products.product_prop,
                       Products.description,
                       Products.profile_url,
                       Products.is_active,
                       Products.current,
                       Products.pictures).where(Products.id < high).where(Products.id >= low)
        result = session.execute(query)
        return [[*i] for i in result], low, high


def pg_insert_new_user(user_id: str, role='user'):
    with Users.session() as session:
        user = Users(
            user_id=user_id,
            group=role
        )
        session.add(user)
        session.commit()
        session.refresh(user)


def pg_select_all_users_id():
    with Users.session() as session:
        query = select(Users.user_id)
        users_id = session.execute(query)
        return [i[0] for i in users_id]


gh_insert(*gh_prepare_data(*pg_select_products(1, 45)))