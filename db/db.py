
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

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
# result = cur.execute('SELECT * FROM transactions;')

###################### GET FUNCTIONS ######################
def get_all_transactions():
    with conn.cursor() as cur:
        result = cur.execute("SELECT * FROM transactions;")
        print(result)
        print(cur.fetchall())
    return result


##################### INSERT and CREATE FUNCTIONS ###################

#TODO: type checking?
#TODO: GLOBAL sql statemtents worth it? Or just repeat?
#Inserts one record(dictionary) using paramatized variables to prevent sql injection
def insert_one(record):
    with conn.cursor() as cur:
        print(f"BEFORE EXECUTE: {record}")

        sql_insert_statement = """
            INSERT INTO transactions (transaction_date, posted_date, card_number, description, category, debited_amount, credited_amount)
            VALUES(%s, %s, %s, %s, %s, %s, %s);
            """
        cur.execute(sql_insert_statement, record)

#Creates transactions table if it doesn't already exist
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

#TODO: See if we can refactor this to be a little cleaner
def insert_many(file="./db/temp_test_csv/december_2022.csv"):
    with open(file, 'r') as file:
        create_transactions_table()
        csvreader = csv.reader(file)
        next(csvreader) #this skips the header
        list_of_record_dicts = []
        for row in csvreader:
            list_of_record_dicts.append(get_obj(row))
        with conn.cursor() as cur:
            sql_insert_statement = """
                INSERT INTO transactions (transaction_date, posted_date, card_number, description, category, debited_amount, credited_amount)
                VALUES(%s, %s, %s, %s, %s, %s, %s);
                """
            cur.executemany(sql_insert_statement, list_of_record_dicts)
        
        
        
        
        

#Used to convert the date format in Capitalone CSVs to date for postgresql
def convert_date(date_string):
    format = "%Y-%m-%d"
    d = datetime.datetime.strptime(date_string, format)
    return d.date()


#Also gives us the option to perform other actions and catch values, like an empty string and convert dates, ect
#TODO I think the logic could be reworked here.
def get_obj(row):
    columns = ['transaction_date', 'posted_date', 'card_number', 'description', 'category', 'debited_amount', 'credited_amount']
    obj = []
    for index in range(len(row)):
        if row[index] == "":
            obj.append(0)
        elif 'date' in columns[index]:
            obj.append(convert_date(row[index]))
        else:
            obj.append(row[index])
    return tuple(obj)


#TODO how are files actually uploaded?
### Testing script to insert data
# with open("./db/temp_test_csv/december_2022.csv", 'r') as file:
#     create_transactions_table()
#     csvreader = csv.reader(file)
#     next(csvreader)

#     for row in csvreader:
#         print(row)
#         obj = get_obj(row)
#         # print(obj)
#         insert_one(obj)
        
insert_many()

