
import os
import psycopg2
import csv
import datetime
from pathlib import Path
from dotenv import load_dotenv

secret = Path(".env")
load_dotenv(secret)

conn = psycopg2.connect(
        host="localhost",
        database="finances",
        user=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'))

conn.autocommit = True
cur = conn.cursor()

class User():

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @classmethod
    def get_by_id(cls, id):
        with conn.cursor() as cur: 
            sql = "SELECT * from users where id = %s;"
            cur.execute(sql, (id,))
            result = cur.fetchall()
        if result:
            return result
        return None

    def is_authenticated(cls, email, password):
        #TODO emails need to be unique
        pass

    def login_user():
        pass
        

print(User.get_by_id(10))