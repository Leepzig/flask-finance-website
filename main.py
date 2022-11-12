from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# testing df display:
dataframe = pd.read_csv("./static/October_2022.csv")
def group_by_category(df):
    df['Category_count'] = df.groupby('Category')['Category'].transform('count')
    columns = ["Category", "Debit", "Category_count"]
    summary = df.groupby([columns[0], columns[2]], as_index=False).sum().sort_values(columns[1])
    return summary.loc[:, summary.columns.isin(columns)]


@app.route("/")
def hello_world():
    return render_template("spread_sheet.html", dataframe=group_by_category(dataframe))

@app.route("/login")
def login():
    return render_template("auth/login.html")