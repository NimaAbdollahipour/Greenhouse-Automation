from . import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    greenhouses = db.relationship('Greenhouse', backref='user')

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    max_temp = db.Column(db.Integer)
    min_temp = db.Column(db.Integer)
    day_length = db.Column(db.Integer)
    light = db.Column(db.Integer)
    moisture = db.Column(db.Integer)
    irrigation = db.Column(db.Integer)
    greenhouses = db.relationship('Greenhouse', backref='plant')

    def __init__(self, name, max_temp, min_temp, day_length, light, moisture, irrigation, user_id):
        self.name = name
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.day_length = day_length
        self.light = light
        self.moisture = moisture
        self.irrigation = irrigation
        self.user_id = user_id


class Greenhouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    temp = db.Column(db.String(120))
    light = db.Column(db.String(120))
    moisture = db.Column(db.Integer)
    tank = db.Column(db.Boolean)
    plant_id = db.Column(db.Integer,db.ForeignKey('plant.id'))
    s_irr_t = db.Column(db.Boolean)
    time1 = db.Column(db.Time)
    time2 = db.Column(db.Time)
    email_enabled = db.Column(db.Boolean, default=True)
    pump = db.Column(db.Boolean, default=True)
    fan = db.Column(db.Boolean, default=True)
    heater = db.Column(db.Boolean,default=True)
    tasks = db.relationship('Task', backref='greenhouse')

    def __init__(self, user_id, temp, light,moisture, tank, plant_id, s_irr_t, time1, time2):
        self.user_id = user_id
        self.temp = temp
        self.light = light
        self.moisture = moisture
        self.tank = tank
        self.plant_id = plant_id
        self.s_irr_t = s_irr_t
        self.time1 = time1
        self.time2 = time2


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(120))
    date_time = db.Column(db.DateTime)
    greenhouse_id = db.Column(db.Integer,db.ForeignKey('greenhouse.id'))

    def __init__(self, command, date_time, greenhouse_id):
        self.command = command
        self.date_time = date_time
        self.greenhouse_id = greenhouse_id
