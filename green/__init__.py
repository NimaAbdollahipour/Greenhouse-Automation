from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NAGREENAUTOFALLwinter20212022'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from .models import User,Plant,Task,Greenhouse
db.create_all()
from .auth import auth
app.register_blueprint(auth,url_prefix = "/auth")
from .green import green
app.register_blueprint(green,url_prefix = "/green")

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