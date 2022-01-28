from flask.helpers import flash
from flask_app import app
from flask import render_template, redirect, session, request
from flask_bcrypt import Bcrypt
from flask_app.controllers import goal
from flask import flash
from flask_app.models.goals import Goal
from flask_app.models.users import User
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    if "loggedin" in session:
        if session["loggedin"] == True:
            return redirect("/dashboard")
    return render_template("index.html")

# methods=["POST"]


@app.route("/register", methods=['POST'])
def reg():
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "name": f'{request.form["first_name"]}, {request.form["last_name"]}',
        "email": request.form['email'],
        "username": request.form['username'],
        "pw_hash": request.form['password'],
        "confirm": request.form['confirm']
    }

    if User.validate_input(data):
        data['pw_hash'] = bcrypt.generate_password_hash(
            request.form['password']).decode('utf8')
        print(data['pw_hash'])
        User.register(data)
    return redirect("/")


@app.route("/login", methods=['POST'])
def login():
    data = {
        "userToken": request.form['userToken'],
        "pword": request.form['pword'],
    }
    if data['pword'] == "":
        flash("please enter a Username or Email and a password", "login")
        return redirect("/")
    else:
        if User.checkUser(data) != False:
            if not bcrypt.check_password_hash(User.checkUser(data), data['pword']):
                flash("password does not match", "login")
                return redirect("/")
            else:

                session['id'] = User.getuserinfo(data)['id']
                session['first_name'] = User.getuserinfo(data)['first_name']
                session['last_name'] = User.getuserinfo(data)['last_name']
                session["loggedin"] = True
                return redirect("/")
        else:
            return redirect("/")


@app.route("/logout")
def logout():
    session["loggedin"] = False
    return redirect("/")
