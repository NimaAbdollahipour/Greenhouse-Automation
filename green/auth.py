from flask import *
import flask
from .models import User
from . import db
auth = Blueprint("auth",__name__)



@auth.route('/login', methods= ["POST", "GET"])
def login():
    if request.method == 'POST':
        db_res = User.query.filter_by(username = request.form['username']).all()
        print(User.query.filter_by(username = request.form['username']).all())
        if len(db_res)>0:
            if db_res[0].password == request.form['password']:
                session['username'] = request.form['username']
                return redirect(url_for('green.monitor'))
            else:
                flash("Wrong Password")
                return redirect(url_for('auth.login'))
        else:
            flash("Wrong Username")
            return redirect(url_for('auth.login'))
    else:
        return render_template('login.html')




@auth.route('/signup', methods = ["POST", "GET"])
def signup():
    if request.method == 'POST':
        db_res = User.query.filter_by(username = request.form['username']).all()
        if len(db_res)>0:
            flash("Username Exists!")
            return redirect(url_for('auth.signup'))
        elif request.form['password'] != request.form['password2']:
            flash("Passwords didn't match!")
            return redirect(url_for('auth.signup'))
        else:
            flash("Wrong Username")
            db.session.add(User(
                request.form['name'],
                request.form['email'],
                request.form['username'],
                request.form['password']
            ))
            db.session.commit()
            return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html')



@auth.route('/logout', methods=["POST"])
def logout():
    if session['username']:
        session.pop('username')
        return redirect(url_for('auth.login'))