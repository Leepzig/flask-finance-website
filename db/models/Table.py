
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
        password=os.environ.get('DB_PASSWORD'),
        autocommit=True)


class Table():

    def __init__(self, start_date=None, end_date=None):
        self.start_date = start_date
        self.end_date = end_date
        self.results = None # results will be what we check for when to display something
    
    def details(self):
        with conn.cursor() as cur:
            columns = ["transaction_date", "category", "description", "debited_amount"]
            sql = """ SELECT transaction_date, category, description, debited_amount FROM transactions
                WHERE transaction_date between %s and %s
            """

            cur.execute(sql, (self.start_date, self.end_date))
            result = cur.fetchall()
        return {"table": result, "total":get_total(result, 3), "columns":columns}


###################### GET FUNCTIONS ######################


def get_transactions_in_specified_time(start_date, end_date):
    with conn.cursor() as cur:
        columns = ["transaction_date", "category", "description", "debited_amount"]
        sql = """ SELECT transaction_date, category, description, debited_amount FROM transactions
            WHERE transaction_date between %s and %s
        """

        cur.execute(sql, (start_date, end_date))
        result = cur.fetchall()
    return {"table": result, "total":get_total(result, 3), "columns":columns}

def get_transactions_summary_timeframe(start_date, end_date):
    with conn.cursor() as cur:
        sql = """SELECT category, sum(debited_amount) totals FROM (SELECT transaction_date, category, description, debited_amount FROM transactions
            WHERE transaction_date between %s and %s) AS all_records
            GROUP BY category 
            ORDER BY totals DESC;
        """

        columns = ['category', 'totals']
        cur.execute(sql, (start_date, end_date))
        result = cur.fetchall()
        return {"table":result, "total":get_total(result, 1), "columns":columns}

#returns a table of data uploaded within the past minute
def get_recently_uploaded_data():
    with conn.cursor() as cur:
        sql = """SELECT transaction_date, category, description, debited_amount FROM transactions
        WHERE created_at >= (NOW() - '1 minute'::interval) AND created_at <= now();"""
        columns = ["transaction_date", "category", "description", "debited_amount"]
        cur.execute(sql)
        result = cur.fetchall()
        return {"table":result, "total":get_total(result, 3), "columns":columns}


##################### Data Manipulation Helper Functions ##############

def get_total(rows, amount_index):
    total = 0
    for line in rows:
        total+= line[amount_index]
    return total

##################### INSERT and CREATE FUNCTIONS ###################

#TODO: type checking?
#TODO: GLOBAL sql statemtents worth it? Or just repeat?
#Inserts one record(dictionary) using paramatized variables to prevent sql injection
def insert_one(record):
    with conn.cursor() as cur:
        sql_insert_statement = """
            INSERT INTO transactions (transaction_date, posted_date, card_number, description, category, debited_amount, credited_amount, created_at)
            VALUES(%s, %s, %s, %s, %s, %s, %s, current_timestamp);
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
        Credited_Amount numeric(10,2),
        created_at timestamp default current_timestamp
        );
        COMMIT;
        """)

#TODO: See if we can refactor this to be a little cleaner
def insert_many(file):
    with open(file, 'r') as file:
        create_transactions_table()
        csvreader = csv.reader(file)
        next(csvreader) #this skips the header
        list_of_record_dicts = []
        for row in csvreader:
            if row:
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
        

