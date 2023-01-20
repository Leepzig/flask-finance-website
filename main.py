from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.utils import secure_filename
import db.db as db
import os

UPLOAD_FOLDER = "./db/temp_csv"
ALLOWED_EXTENSIONS = {"csv"}
#TODO decide max size of temp files
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

##########Routes##################

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/upload", methods=["POST", "GET"])
def upload_file():
    print(request.files)
    test = 'file' not in request.files
    print(f"TESTTTTTTTTT: {test}")
    if request.method=="POST":
        if 'file' not in request.files:
            flash('No file chosen')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No Selected File')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            ## what to do after this?
        return render_template("spread_sheet.html", dataframe=db.get_transactions_in_specified_time("2022-12-1", "2022-12-31"))
    return render_template("upload.html")

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