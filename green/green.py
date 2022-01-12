from flask import *
import flask
from .models import User,Greenhouse,Plant,Task
from . import db
from datetime import *
green = Blueprint("green",__name__)

@green.route('/monitor',methods=["POST","GET"])
def monitor():
    if session.get('username', None):
        return render_template('monitor.html')
    return redirect(url_for('auth.login'))



@green.route('/new_plant',methods=["POST","GET"])
def new_plant():
    if session.get('username', None):
        if request.method == "POST":
            for key,value in request.form.items():
                if len(value.strip()) == 0:
                    flash(key+"is not valid")
                    return redirect(url_for('green.new_plant'))
            user = User.query.filter_by(username = session['username']).all()
            db.session.add(Plant(
                request.form['name'],
                request.form['max_temp'],
                request.form['min_temp'],
                request.form['day_length'],
                request.form['light'],
                request.form['moisture'],
                request.form['irrigation'],
                user[0].id
            ))
            db.session.commit()
            flash("Plant Created Successfuly!")
            return redirect(url_for('green.new_plant'))
        else:
            return render_template('plant.html')
    return redirect(url_for('auth.login'))




@green.route('/greenhouse',methods=["POST"])
def greenhouse():
    if session['username']:
        pass
    else:
        redirect(url_for('auth.login'))




@green.route('/tasks',methods=["POST","GET"])
def tasks():
    if session['username']:
        if request.method == "POST":
            db.session.add(Task(
                request.form['command'],
                datetime.now(),
                User.query.filter_by(username = session['username']).first().id
                ))
            db.session.commit()
        else:
            tasks = Task.query.filter_by(id=User.query.filter_by(username = session['username']).first().id).all()
            return render_template('tasks.html',task_list = tasks)
    else:
        redirect(url_for('auth.login'))