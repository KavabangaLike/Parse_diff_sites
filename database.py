import random
import sqlite3
import uuid


class DataBase:
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    @classmethod
    def get(cls, item_to_select):
        sql = f'SELECT {item_to_select} FROM products'
        return cls.cursor.execute(sql)

    @classmethod
    def post(cls, data):
        sql_insert = 'INSERT INTO products(id, product_link, title, price, product_prop, description, profile_url, pictures, current) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cls.cursor.execute(sql_insert, (random.randint(1, 999999), data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],))
        cls.connection.commit()

