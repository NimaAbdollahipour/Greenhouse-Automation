
import email
import re
from flask import *
import flask
from .models import User,Greenhouse,Plant,Task
from . import db
from datetime import *
green = Blueprint("green",__name__)

@green.route('/monitor',methods=["GET"])
def monitor():
    if session.get('username', None):
        g = Greenhouse.query.filter_by(user = session['id']).first()
        s = Plant.query.get(g.plant)
        return render_template('monitor.html',green = g,selected = s)
    return redirect(url_for('auth.login'))

@green.route('/new_plant',methods=["POST","GET"])
def new_plant():
    if session.get('username', None):
        if request.method == "POST":
            for key,value in request.form.items():
                if len(value.strip()) == 0:
                    flash(key+" is not valid")
                    return redirect(url_for('green.new_plant'))
            db.session.add(Plant(
                request.form['name'],
                request.form['max_temp'],
                request.form['min_temp'],
                request.form['day_length'],
                request.form['light'],
                request.form['moisture'],
                request.form['irrigation'],
                session['id']
            ))
            db.session.commit()
            flash("Plant Created Successfuly!")
            return redirect(url_for('green.new_plant'))
        else:
            return render_template('plant.html')
    return redirect(url_for('auth.login'))




@green.route('/config',methods=["POST","GET"])
def config():
    if session.get('username',None):
        if request.method =="GET":
            p = Plant.query.all()
            g = Greenhouse.query.filter_by(user = session['id']).first()
            s = Plant.query.get(g.plant)
            return render_template('config.html',plants=p,green = g,selected =s)
        else:
            g = Greenhouse.query.filter_by(user = session['id']).first()
            if request.form.get('sp_time',None):
                Greenhouse.query.get(g.id).s_irr_t = True
            else:
                Greenhouse.query.get(g.id).s_irr_t = False
            if request.form.get('time1',None):
                t = request.form['time1'].split(':')
                Greenhouse.query.get(g.id).time1 = time(int(t[0]),int(t[1]))
            if request.form.get('time2',None):
                t = request.form['time2'].split(':')
                Greenhouse.query.get(g.id).time2 = time(int(t[0]),int(t[1]))
            if request.form.get('plant',None):
                Greenhouse.query.get(g.id).plant = request.form['plant']
            db.session.commit()
            return redirect(url_for('green.config'))

    else:
        return redirect(url_for('auth.login'))


@green.route('/account_config', methods=['POST'])
def account_config():
    if session.get('username',None):
        c = ['0','0','0','0','0']
        res = request.form
        if res.get('email',None):
            c[0] = '1'
        if res.get('email_status',None):
            c[1] = '1'
        if res.get('email_temp',None):
            c[2] = '1'
        if res.get('email_light',None):
            c[3] = '1'
        if res.get('email_tank',None):
            c[4] = '1'
        c = ''.join(c)
        User.query.get(session['id']).config = c
        db.session.commit()
        return redirect(url_for('green.tasks'))
    else:
        return redirect(url_for('auth.login'))



@green.route('/tasks',methods=["POST","GET"])
def tasks():
    if session.get('username',None):
        if request.method == "POST":
            db.session.add(Task(
                request.form['command'],
                datetime.now(),
                User.query.filter_by(username = session['username']).first().id
                ))
            db.session.commit()
            return redirect(url_for('green.tasks'))
        else:
            conf = User.query.get(session['id']).config
            conf = list(conf)
            for i in range(len(conf)):
                conf[i] = int(conf[i])
            return render_template('tasks.html',config=conf)
    else:
        redirect(url_for('auth.login'))
