from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
app = Flask(__name__)
app.config['SECRET_KEY'] = 'NAGREENAUTOFALLwinter20212022'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#----Email Configuration---------------------------------------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'example@gmail.com'
app.config['MAIL_PASSWORD'] = 'gfaodzqgrcbsfsqh'
app.config['MAIL_DEFAULT_SENDER'] = 'example@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False
ml = Mail(app)

from .models import User,Plant,Task,Greenhouse
db.create_all()
from .auth import auth
app.register_blueprint(auth,url_prefix = "/auth")
from .green import green
app.register_blueprint(green,url_prefix = "/green")
from .data_exc import data_exc
app.register_blueprint(data_exc,url_prefix="/dataexchange")

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

@app.route('/tasks')
def tasks():
    if session.get('username', None):
        return render_template('tasks.html')
    return redirect(url_for('home'))

@app.route('/addplant', methods=['POST','GET'])
def add_plant():
    if session.get('username', None):
        return render_template('monitor.html')
    return redirect(url_for('home'))