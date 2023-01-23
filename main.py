from flask import Flask, render_template, request, url_for, flash, redirect
from flask_navigation import Navigation
from werkzeug.utils import secure_filename
import db.db as db
import os
from flask_jwt_router import JwtRoutes
from pathlib import Path
from dotenv import load_dotenv
from flask import session
from flask_login import LoginManager
from db.models.User import User

login_manager = LoginManager()

secret = Path(".env")
load_dotenv(secret)
secret_key = os.environ.get('SECRET_SECRET')


UPLOAD_FOLDER = "./db/temp_csv"
ALLOWED_EXTENSIONS = {"csv"}
#TODO decide max size of temp files
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

app = Flask(__name__)
nav = Navigation(app)
app.secret_key = secret_key
login_manager.init_app(app)
# JwtRoutes(app)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config["WHITE_LIST_ROUTES"] = [
#     ("POST", "/register"),
#     ("POST", "/login")
# ]

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

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

@app.route('/test')
def test():
    print(session)
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next = request.args.get('next')
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        session['username'] = username
        print(session)

        if authenticate(app.config['AUTH_SERVER'], username, password):
            user = User.query.filter_by(username=username).first()
            if user:
                if login_user(DbUser(user)):
                    # do stuff
                    flash("You have logged in")

                    return redirect(next or url_for('index', error=error))
        error = "Login failed"
    return render_template('auth/login.html', login=True, next=next, error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# @app.route("/register", methods=["POST"])
# def register():
#     user_data = request.get_json()
#     try:
#         user = UserModel(**user_data)
#         user.create_user() # your entity creation logic

#         # Here we pass the id as a kwarg to `register_entity`
#         token: str = jwt_routes.register_entity(entity_id=user.id, entity_type="users")

#         # Now we can return a new token!
#         return {
#             "message": "User successfully created.",
#             "token": str(token),  # casting is optional
#         }, 200