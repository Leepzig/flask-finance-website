from flask import Flask, render_template
import pandas as pd
from utils.capital_one_transactions_dataframe import Transactions_Dataframe
# from utils.capital_one_transactions_dataframe import grp

app = Flask(__name__)

# testing df display:
dataframe = pd.read_csv("./temp_test_csv/October_2022.csv")

df = Transactions_Dataframe.Transactions_Dataframe("./db/temp_test_csv/October_2022.csv")



@app.route("/")
def hello_world():
    return render_template("spread_sheet.html", dataframe=df.group_by_category())

@app.route("/login")
def login():
    return render_template("auth/login.html")