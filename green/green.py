from flask import *
import flask
from .models import User,Greenhouse,Plant,Task
from . import db
from datetime import *
from .auth import login_required

green = Blueprint("green",__name__)

@green.route('/monitor',methods=["GET"])
@login_required
def monitor():
    g = Greenhouse.query.filter_by(user_id = session['id']).first()
    s = Plant.query.get(g.plant_id)
    return render_template('monitor.html',green = g,selected = s)

@green.route('/new_plant',methods=["POST","GET"])
@login_required
def new_plant():
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




@green.route('/config',methods=["POST","GET"])
@login_required
def config():
    if request.method =="GET":
        p = Plant.query.all()
        g = Greenhouse.query.filter_by(user_id = session['id']).first()
        s = Plant.query.get(g.plant_id)
        return render_template('config.html',plants=p,green = g,selected =s)
    else:
        g = Greenhouse.query.filter_by(user_id = session['id']).first()
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
            Greenhouse.query.get(g.id).plant_id = request.form['plant']
        db.session.commit()
        return redirect(url_for('green.config'))


@green.route('/account_config', methods=['POST'])
@login_required
def account_config():
    res = request.form
    g = Greenhouse.query.filter_by(user_id = session['id']).first()
    if res.get('email'):
        g.email_enabled = True
    else:
        g.email_enabled = False


    if res.get('fan'):
        g.fan = True
    else:
        g.fan = False


    if res.get('pump'):
        g.pump = True
    else:
        g.pump = False


    if res.get('heater'):
        g.heater = True
    else:
        g.heater = False

    db.session.commit()
    return redirect(url_for('green.tasks'))



@green.route('/tasks',methods=["POST","GET"])
@login_required
def tasks():
    if request.method == "POST":
        db.session.add(Task(
            request.form['command'],
            datetime.now(),
            User.query.get(session['id']).greehouses[0]
        ))
        db.session.commit()
        return redirect(url_for('green.tasks'))
    else:
        g = Greenhouse.query.filter_by(user_id = session['id']).first()
        return render_template('tasks.html',gr = g)