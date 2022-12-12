
import os
import psycopg2
import csv
import datetime

conn = psycopg2.connect(
        host="localhost",
        database="financewebapp",
        user=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'))

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
result = cur.execute('SELECT * FROM transactions;')


def get_all_transactions():
    with conn.cursor() as cur:
        result = cur.execute("SELECT * FROM transactions;")
    return result

#TODO: type checking?
def insert_one(record):
    with conn.cursor() as cur:
        cur.execute(f"""
        INSERT INTO transactions (transaction_date, posted_date, card_number, description, category, debited_amount, credited_amount)
        VALUES('{record['transaction_date']}'::date,'{record['posted_date']}'::date,{record['card_number']},'{record['description']}','{record['category']}',{record['debited_amount']},{record['credited_amount']})
        """)

def create_transactions_table():
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXIST Transactions
        (id serial primary key, 
        Transaction_Date date, 
        Posted_Date date, 
        Card_Number int, 
        Description text, 
        Category varchar(30), 
        Debited_Amount numberic(4,2), 
        Credited_Amount numeric(4,2)
        );
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
            obj[keys[index]] = 'Null'
        elif 'date' in keys[index]:
            obj[keys[index]] = convert_date(row[index])
        else:
            obj[keys[index]] = row[index]
    return obj

with open("./db/temp_test_csv/August_2022.csv", 'r') as file:
  csvreader = csv.reader(file)
  next(csvreader)

  for row in csvreader:
    obj = get_obj(row)
    print(obj)
    insert_one(obj)
    break


