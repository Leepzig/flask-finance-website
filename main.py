from flask import Flask, render_template, request, url_for
# import pandas as pd
# from utils.capital_one_transactions_dataframe import Transactions_Dataframe
import db.db as db
# from utils.capital_one_transactions_dataframe import grp

app = Flask(__name__)

# testing df display:
# dataframe = pd.read_csv("./temp_test_csv/October_2022.csv")

# file = db.get_csv("October_2022.csv")

# df = Transactions_Dataframe.Transactions_Dataframe(file["file"])
dataframe=db.get_transactions_summary_timeframe('2022-12-1','2022-12-31')
print(f"LINE 16 {dataframe}")


@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/home", methods=["POST", "GET"])
def get_table():
    if request.method == "POST":
        print(request.form)
        if request.form['table_type'] == 'summary':
            return render_template("spread_sheet.html", dataframe=db.get_transactions_summary_timeframe(request.form['start_date'], request.form['end_date']))
        elif request.form['table_type'] == 'details':
            return render_template("spread_sheet.html", dataframe=db.get_transactions_in_specified_time(request.form['start_date'], request.form['end_date']))
    else:
        return render_template("index.html")

@app.route("/login")
def login():
    return render_template("auth/login.html")