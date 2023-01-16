
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

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
# result = cur.execute('SELECT * FROM transactions;')


def get_all_transactions():
    with conn.cursor() as cur:
        result = cur.execute("SELECT * FROM transactions;")
    return result

#TODO: type checking?
def insert_one(record):
    with conn.cursor() as cur:
        print(f"BEFORE EXECUTE: {record}")
        cur.execute("""
            INSERT INTO transactions (transaction_date, posted_date, card_number, description, category, debited_amount, credited_amount)
            VALUES(%s, %s, %s, %s, %s, %s, %s);
            """, (record['transaction_date'], record['posted_date'], record['card_number'], record['description'], record['category'], record['debited_amount'], record['credited_amount']))

def create_transactions_table():
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Transactions
        (id serial primary key, 
        Transaction_Date date, 
        Posted_Date date, 
        Card_Number int, 
        Description text, 
        Category varchar(30), 
        Debited_Amount numeric(10,2), 
        Credited_Amount numeric(10,2)
        );
        COMMIT;
        """)

#TODO: calling insert_one over and over is probably bad practice and not effcient at all, rework.
def insert_many(records):
    with conn.cursor() as cur:
        for r in records:
            insert_one(r)



def convert_date(date_string):
    format = "%Y-%m-%d"
    d = datetime.datetime.strptime(date_string, format)
    return d.date()

def get_obj(row):
    keys = ['transaction_date', 'posted_date', 'card_number', 'description', 'category', 'debited_amount', 'credited_amount']
    obj = {}
    for index in range(len(row)):
        if row[index] == "":
            obj[keys[index]] = 0
        elif 'date' in keys[index]:
            obj[keys[index]] = convert_date(row[index])
        else:
            obj[keys[index]] = row[index]
    return obj




with open("./db/temp_test_csv/december_2022.csv", 'r') as file:
    create_transactions_table()
    csvreader = csv.reader(file)
    next(csvreader)

    for row in csvreader:
        print(row)
        obj = get_obj(row)
        # print(obj)
        insert_one(obj)
        


