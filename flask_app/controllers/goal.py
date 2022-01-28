from flask.globals import g
from flask.helpers import flash
from flask_app.models.users import User
from flask_app.models.goals import Goal, Specifics, Breakdown
from flask_app import app
from flask import render_template, redirect, session, request
from flask import flash


@app.route("/dashboard")
def dashboard():
    data = {"id": session['id']}
    specifics = Specifics.user_has_specifics(data)
    data2 = []
    for specific in specifics:
        dict = {
            "specid": specific["specifics_id"],
            "id": specific["user_id"]
        }
        data2.append(dict)
    goals = []
    for thing in data2:
        result = Goal.get_all_info_by_user_id(thing)
        if result != None:
            goal = result[0]
            goals.append(goal)
    # print(goals)
    return render_template("dashboard.html", goals=goals)


@app.route("/goals")
def goals():
    data = {"id": session['id']}
    specifics = Specifics.user_has_specifics(data)
    data2 = []
    for specific in specifics:
        dict = {
            "specid": specific["specifics_id"],
            "id": specific["user_id"]
        }
        data2.append(dict)
    goals = []
    for thing in data2:
        result = Goal.get_all_info_by_user_id(thing)
        if result != None:
            goal = result[0]
            goals.append(goal)
    return render_template("goals.html", goals=goals)


@app.route("/view/goal/<int:id>")
def viewgoal(id):
    # get goal name
    goalid = {
        "id": id
    }
    goalname = Goal.getgoalnamebyid(goalid)['name']
    # get specifics why
    specdata = {
        'goalid': id,
        "userid": session['id']
    }
    why = Specifics.getwhy(specdata)['why']
    # get all breakdowns (before today)
    specid = Specifics.user_has_specificsid(specdata)['specifics_id']
    print(specid)
    data = {
        "id": session['id'],
        "specid": specid,
        "goal_id": id
    }
    beforetoday = Goal.get_all_breakdowns_before(data)
    aftertoday = Goal.get_all_breakdowns_after(data)
    # get all breakdowns (after/including today)
    return render_template("goal.html", id=id,  beforetoday=beforetoday, aftertoday=aftertoday)


@app.route("/goal/new")
def newgoal():
    goals = Goal.getAllPublicGoals()
    return render_template("newgoal.html", goals=goals)


@app.route('/didit/<int:bdid>/<int:gid>')
def didit(bdid, gid):
    data = {
        "id": bdid
    }
    Breakdown.didit(data)
    return redirect(f'/view/goal/{gid}')


@app.route('/undid/<int:bdid>/<int:gid>')
def undid(bdid, gid):
    data = {
        "id": bdid
    }
    Breakdown.undid(data)
    return redirect(f'/view/goal/{gid}')


@app.route('/add/new/goal/', methods=["POST"])
def newgoalsubmit():
    print("this is the post request ", request.form)
    if "check" in request.form:
        ispublic = 1
    else:
        ispublic = 0
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "ispublic": ispublic
    }
    print("this is data", data)

    id = Goal.registerGoal(data)
    print('this is id', id)
    return redirect(f'/specifics/{id}')


@app.route('/add/public/goal/', methods=["POST"])
def publicgoalsubmit():
    id = request.form["id"]

    return redirect(f'/specifics/{id}')


@app.route('/specifics/<int:id>')
def specifics(id):
    id = id
    return render_template('specifics.html', id=id)


@app.route('/specifics/<int:id>/submit', methods=["POST"])
def specificssubmit(id):
    data = {
        "due_date": request.form['date'],
        "mqd": request.form['mqd'],
        "why": request.form["why"]
    }
    specid = Specifics.registerspecifics(data)
    print(specid)
    data2 = {
        "user_id": session["id"],
        "goal_id": id,
        "specifics_id": specid
    }
    Goal.newuserhasgoal(data2)

    return redirect(f'/breakdowns/{specid}')


@app.route('/breakdowns/<int:id>')
def breakdowns(id):
    id = id
    return render_template('breakdowns.html', id=id)


@app.route('/breakdowns/<int:id>/submit', methods=["POST"])
def breakdownssubmit(id):
    print(request.form)
    specid = id
    raw_breakdowns = list(zip(request.form.getlist(
        'date'), (request.form.getlist('mqd'))))
    for raw in raw_breakdowns:
        data = {
            'specifics_id': specid,
            'date': raw[0],
            'mqd': raw[1]
        }
        print(data)
        Breakdown.new_breakdown(data)
    return redirect('/dashboard')
