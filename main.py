from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NAGREENAUTOFALLwinter20212022'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password


class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    user = db.Column(db.Integer)
    max_temp = db.Column(db.Integer)
    min_temp = db.Column(db.Integer)
    day_length = db.Column(db.Integer)
    light = db.Column(db.Integer)
    moisture = db.Column(db.Integer)
    irrigation = db.Column(db.Integer)

    def __init__(self, name, max_temp, min_temp, day_length, light, moisture, irrigation, user):
        self.name = name
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.day_length = day_length
        self.light = light
        self.moisture = moisture
        self.irrigation = irrigation
        self.user


class Greenhouse(db.Model):
    __tablename__ = 'greenhouse'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer)
    temp = db.Column(db.String(120))
    light = db.Column(db.String(120))
    tank = db.Column(db.Boolean)
    plant = db.Column(db.Integer)
    s_irr_t = db.Column(db.Boolean)
    time1 = db.Column(db.Time)
    time2 = db.Column(db.Time)

    def __init__(self, user, temp, light, tank, plant, s_irr_t, time1, time2):
        self.user = user
        self.temp = temp
        self.light = light
        self.tank = tank
        self.plant = plant
        self.s_irr_t = s_irr_t
        self.time1 = time1
        self.time2 = time2


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(120))
    date_time = db.Column(db.DateTime)
    user = db.Column(db.Integer)

    def __init__(self, command, date_time, user):
        self.command = command
        self.date_time = date_time
        self.user = user


db.create_all()


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/monitor')
def monitor():
    if session.get('username', None):
        return render_template('monitor.html')
    return redirect(url_for('home'))


@app.route('/new_plant')
def new_plant():
    if session.get('username', None):
        return render_template('plant.html')
    return redirect(url_for('home'))


@app.route('/tasks')
def tasks():
    if session.get('username', None):
        return render_template('tasks.html')
    return redirect(url_for('home'))


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/authenticate', methods=['POST', 'GET'])
def authenticate():
    if request.method == "POST":
        result = request.form
        for key, value in result.items():
            if value:
                for i in User.query.all():
                    if i.username == result['username'] and i.password == result['password']:
                        session['username'] = result['username']
                        return redirect('monitor')
    flash('Wrong password or Username!')
    return redirect(url_for('home'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        result = request.form
        for key, value in result.items():
            if value:
                if len(value) < 4:
                    flash('Short {}'.format(key))
                    return redirect(url_for('signup'))
            else:
                flash('No {} Entered'.format(key))
                return redirect(url_for('signup'))
        if result['password'] != result['password2']:
            flash("Entered Passwords Did Not Match")
            return redirect(url_for('signup'))
        for i in User.query.all():
            if i.username == result['username']:
                flash("Username Is Not Available!")
                return redirect(url_for('signup'))
    user = User(result['name'], result['email'], result['username'], result['password'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


db.create_all()
if __name__ == "__main__":
    app.run(debug=True)
