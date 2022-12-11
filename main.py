from flask import Flask, render_template
import pandas as pd
from utils.capital_one_transactions_dataframe import Transactions_Dataframe
import db.db as db
# from utils.capital_one_transactions_dataframe import grp

app = Flask(__name__)

# testing df display:
# dataframe = pd.read_csv("./temp_test_csv/October_2022.csv")

file = db.get_csv("October_2022.csv")

df = Transactions_Dataframe.Transactions_Dataframe(file["file"])



@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/home")
def hello_world():
    if df in df:
        return render_template("spread_sheet.html", dataframe=df.group_by_category())
    else:
        return render_template("index.html")

@app.route("/login")
def login():
    return render_template("auth/login.html")