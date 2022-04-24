from flask import *
import flask
from .models import Greenhouse, Task, User,Plant
from . import db,ml,app
from datetime import *
from flask_mail import Message
from functools import wraps
import jwt

def token_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		token = request.headers.get('token')
		if not token:
			return jsonify({'message':'token is missing!'}),403
		try:
			data = jwt.decode(token,app.config["SECRET_KEY"],algorithms=["HS256"])
			current_user = User.query.filter_by(username=data.get('user')).first()
		except:
			return jsonify({'message':'Token is invalid'}),403,
		return f(current_user,*args,**kwargs)
	return decorated


data_exc = Blueprint('data_exc',__name__)

@data_exc.route('/data',methods=["POST","GET"])
@token_required
def data_exchange(current_user):
	if request.method=="GET":
		id = request.args.get('id')
		if id:
			g = Greenhouse.query.get(id)
			p = Plant.query.get(g.plant_id)
			if not g:
				return jsonify({'message':'greenhouse not found!'})
			return jsonify({
				"plant_max_temp":p.max_temp,
				"plant_min_temp":p.min_temp,
				"plant_moisture":p.moisture,
				"email":g.email_enabled,
				"fan":g.fan,
				"pump":g.pump,
				"heater":g.heater
				})
		else: 
			return jsonify({"message":"id is missing!"})
	else:
		id = request.json.get('id')
		if id:
			g = Greenhouse.query.get(id)
			if not g:
				return jsonify({'message':'greenhouse not found!'})
			
			light = request.json.get('light')
			temp = request.json.get('temp')
			moisture = request.json.get('moisture')
			tank = request.json.get('tank')
			g.light = str(light)[1:-1]
			g.temp = str(temp)[1:-1]
			g.moisture = moisture
			g.tank = tank
			db.session.commit()
			#current_user.email = 'pejagom301@chinamkm.com'
			send_mail(current_user,g)
			return jsonify({"message":"data saved successfully!"})
		else: 
			return jsonify({"message":"id is missing!"})

@data_exc.route('/login',methods=["POST"])
def login():
	usr = request.json.get('username',None)
	psw = request.json.get('password',None)
	if usr and psw:
		u = User.query.filter_by(username=usr).first()
		if u:
			if psw==u.password:
				token = jwt.encode({'user':usr, 'exp':datetime.utcnow()+timedelta(minutes=30)},
					app.config["SECRET_KEY"],algorithm="HS256") 
				return jsonify({"message":"ok","token":token})
			else:
				return jsonify({"message":"wrong password"})
		else:
			return jsonify({"message":"user not found"})
	else: 
		return jsonify({"message":"data was not complete one or more was missing!"})

@data_exc.route('/tasks',methods=["GET"])
@token_required
def tasks(current_user):
    data_to_send =[]
    tasks_in_db = Task.query.filter_by(user=current_user.id)
    for t in tasks_in_db:
        data_to_send.append(t.command)
        db.session.delete(t)
    return jsonify({"message":"ok","commands":data_to_send})

def send_mail(user,g):
	t = g.temp.split(',')[-1]
	content = [t]
	if int(g.light.split(',')[-1])==1:
		content.append('Low')
	elif int(g.light.split(',')[-1])==2:
		content.append('Medium')
	else:
		content.append('High')

	if g.tank == True:
		content.append('Full')
	else:
		content.append('Empty')
	
	if g.moisture==1:
		content.append('Low')
	elif g.moisture==2:
		content.append('Medium')
	else:
		content.append('High')

	m = message_creator(g)
	content.append(m)
	msg = Message('Greenhouse Automation',recipients=[user.email])
	msg.html = '''<p><b>This message is sent automatically from greenhouse automation
	 server (no-reply)</b></p>
	 <h4 style="color:red">Data:</h4>
	 <b>Temperature: </b><label>{}</label><br/>
	 <b>Light Intensity: </b><label>{}</label><br/>
	 <b>Tank: </b><label>{}</label><br/>
	 <b>Soil Moisture Level: </b><label>{}</label><br/>
	 <h4 style="color:red">Messages:</h4>
	 <p>{}</p>
	 '''.format(content[0],content[1],content[2],content[3],content[4])
	ml.send(msg)
	return 'Message has been sent'

def message_creator(g):
	created_message=''
	p = Plant.query.get(g.plant)
	if  int(g.temp.split(',')[-1]) < p.min_temp:
		created_message += "Temperature is lower than minimum temperature for plant\n"
	elif  int(g.temp.split(',')[-1]) > p.max_temp:
		created_message += "Temperature is higher than maximum temperature for plant\n"
	if len(g.light.split(',')) == 24:
		ok_hours = 0
		for i in g.light.split(','):
			if int(i) >= p.light:
				ok_hours +=1
		if ok_hours<p.day_len:
				created_message+='Light is not enough\n'
	if not g.tank:
		created_message+='Tank is empty\n'
	return created_message
