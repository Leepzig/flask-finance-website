from flask import Flask, render_template, request, url_for, flash, redirect
from flask_navigation import Navigation
from werkzeug.utils import secure_filename
import db.db as db
import os
from flask_jwt_router import JwtRoutes

UPLOAD_FOLDER = "./db/temp_csv"
ALLOWED_EXTENSIONS = {"csv"}
#TODO decide max size of temp files
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

app = Flask(__name__)
nav = Navigation(app)
# JwtRoutes(app)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config["WHITE_LIST_ROUTES"] = [
#     ("POST", "/register"),
#     ("POST", "/login")
# ]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

##########Routes##################

nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('Upload', 'upload_file'),
    nav.Item('Dashboard', 'get_table')
])



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST", "GET"])
def upload_file():
    test = 'file' not in request.files
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
            print(filename)
            print(app.config['UPLOAD_FOLDER'])
            print(file)
            db.insert_many(app.config['UPLOAD_FOLDER']+'/'+filename)
        return render_template("spread_sheet.html", dataframe=db.get_recently_uploaded_data())
    return render_template("upload.html")

@app.route("/dashboard", methods=["POST", "GET"])
def get_table():
    if request.method == "POST":
        if request.form['table_type'] == 'summary':
            return render_template("spread_sheet.html", dataframe=db.get_transactions_summary_timeframe(request.form['start_date'], request.form['end_date']))
        elif request.form['table_type'] == 'details':
            return render_template("spread_sheet.html", dataframe=db.get_transactions_in_specified_time(request.form['start_date'], request.form['end_date']))
    else:
        return render_template("spread_sheet.html", dataframe=[])

@app.route("/login")
def login():
    return render_template("auth/login.html")

@app.route("/register", methods=["POST"])
def register():
    return "I don't need authorizing"