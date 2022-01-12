from . import db
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