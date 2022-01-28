from types import ClassMethodDescriptorType
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Specifics():
    def __init__(self, data):
        self.goal_id = data["goal_id"]
        self.user_id = data["user_id"]
        self.id = data["id"]
        self.due_date = data["due_date"]
        self.mqd = data["mqd"]
        self.satisfied = data["satisfied"]
        self.why = data["why"]
        self.breakdown = None

    @classmethod
    def registerspecifics(cls, data):
        query = "INSERT INTO specifics (due_date,mqd,satisfied,why) VALUES(%(due_date)s,%(mqd)s,0,%(why)s);"
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        return results

    @classmethod
    def getwhy(cls, data):
        query = "select why from specifics join user_has_goal on specifics.id = user_has_goal.specifics_id where user_id= %(userid)s and goal_id = %(goalid)s"
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        return results[0]

    @classmethod
    def user_has_specifics(cls, data):
        query = 'select user_id, specifics_id from user_has_goal where user_id = %(id)s'
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        return results

    @classmethod
    def user_has_specificsid(cls, data):
        query = 'select specifics_id from user_has_goal where goal_id = %(goalid)s and user_id = %(userid)s'
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)[0]
        return results


class Breakdown():
    def __init__(self, data):
        self.specifics_id = data["specifics_id"]
        self.id = data["id"]
        self.due_date = data["due_date"]
        self.mqd = data["mqd"]
        self.satisfied = data["satisfied"]

    @classmethod
    def new_breakdown(cls, data):
        query = "insert into breakdown (due_date, mqd, satisfied, specifics_id) values(%(date)s,%(mqd)s,0,%(specifics_id)s)"
        print(query)
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        return results

    @classmethod
    def didit(cls, data):
        query = "update breakdown SET satisfied = 1 where id = %(id)s"
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        return results

    @classmethod
    def undid(cls, data):
        query = "update breakdown SET satisfied =0 where id = %(id)s"
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        return results


class Goal():
    def __init__(self, data):
        self.id = data["goal_id"]
        self.name = data["goal_name"]
        self.description = data["goal_description"]
        self.ispublic = data["ispublic"]
        self.specifics = None

    @classmethod
    def registerGoal(cls, data):
        query = "INSERT INTO goal (name,description,ispublic) VALUES(%(name)s,%(description)s,%(ispublic)s);"
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        print(results)
        return results

    @classmethod
    def getgoalnamebyid(cls, data):
        query = "select name from goal where id = %(id)s"
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        return results[0]

    @classmethod
    def getAllPublicGoals(cls):
        query = "select * from goal where ispublic = 1"
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query)
        goals = []
        for result in results:
            result["goal_id"] = result["id"]
            del result["id"]
            result["goal_name"] = result["name"]
            del result["name"]
            result["goal_description"] = result["description"]
            del result["description"]
            goal = cls(result)
            goals.append(goal)
        return goals

    @classmethod
    def newuserhasgoal(cls, data):
        query = "INSERT INTO user_has_goal (user_id,goal_id,specifics_id)VALUES(%(user_id)s,%(goal_id)s,%(specifics_id)s);"
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        print(results)
        return results

    @classmethod
    def get_all_info_by_user_id(cls, data):
        goals = []
        query = "select goal.id as goal_id, goal.name as goal_name,goal.description as goal_description, goal.ispublic as ispublic,user_has_goal.user_id as  user_id, specifics.id as specifics_id, specifics.due_date as specifics_duedate, specifics.due_date as specifics_due_date, specifics.mqd as specifics_mqd, specifics.satisfied as specifics_satisfied, breakdown.due_date as breakdown_due_date, why, breakdown.id as breakdown_id, breakdown.mqd as breakdown_mqd, breakdown.satisfied as breakdown_satisfied   from goal join user_has_goal on user_has_goal.goal_id=goal.id join specifics on user_has_goal.specifics_id = specifics.id join breakdown on user_has_goal.specifics_id=breakdown.specifics_id where user_has_goal.user_id =%(id)s and breakdown.due_date>=CURDATE() and specifics.id=%(specid)s and breakdown.satisfied=0"

        connection = connectToMySQL('didthedamnthing')
        result = connection.query_db(query, data)
        print('this is result', result)
        if result != ():
            result = result[0]
        else:
            return None
        goal = cls(result)
        specifics_data = {
            "goal_id": result["goal_id"],
            "user_id": result["user_id"],
            "id": result["specifics_id"],
            "due_date": result["specifics_due_date"],
            "mqd": result["specifics_mqd"],
            "satisfied": result["specifics_satisfied"],
            "why": result["why"]
        }
        breakdown_data = {
            "id": result["breakdown_id"],
            "specifics_id": result["specifics_id"],
            "due_date": result["breakdown_due_date"],
            "mqd": result["breakdown_mqd"],
            "satisfied": result["breakdown_satisfied"],
        }
        goal.specifics = Specifics(specifics_data)
        goal.specifics.breakdown = Breakdown(breakdown_data)
        goals.append(goal)
        print(goals)
        return goals

    @classmethod
    def newuserhasgoal(cls, data):
        query = "INSERT INTO user_has_goal (user_id,goal_id,specifics_id)VALUES(%(user_id)s,%(goal_id)s,%(specifics_id)s);"
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        print(results)
        return results

    @classmethod
    def get_all_breakdowns_after(cls, data):
        goals = []
        query = 'SELECT goal.id AS goal_id, goal.name AS goal_name, goal.description AS goal_description, goal.ispublic AS ispublic, user_has_goal.user_id AS user_id, specifics.id AS specifics_id, specifics.due_date AS specifics_duedate, specifics.due_date AS specifics_due_date, specifics.mqd AS specifics_mqd, specifics.satisfied AS specifics_satisfied, breakdown.due_date AS breakdown_due_date, why, breakdown.id AS breakdown_id, breakdown.mqd AS breakdown_mqd, breakdown.satisfied AS breakdown_satisfied FROM goal JOIN user_has_goal ON user_has_goal.goal_id = goal.id JOIN specifics ON user_has_goal.specifics_id = specifics.id JOIN breakdown ON user_has_goal.specifics_id = breakdown.specifics_id WHERE user_has_goal.user_id = %(id)s  and breakdown.due_date>=CURDATE() and specifics.id=%(specid)s and goal_id =%(goal_id)s '
        print(query)
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        goals = []
        for result in results:
            goal = cls(result)
            specifics_data = {
                "goal_id": result["goal_id"],
                "user_id": result["user_id"],
                "id": result["specifics_id"],
                "due_date": result["specifics_due_date"],
                "mqd": result["specifics_mqd"],
                "satisfied": result["specifics_satisfied"],
                "why": result["why"]
            }
            breakdown_data = {
                "id": result["breakdown_id"],
                "specifics_id": result["specifics_id"],
                "due_date": result["breakdown_due_date"],
                "mqd": result["breakdown_mqd"],
                "satisfied": result["breakdown_satisfied"],
            }
            goal.specifics = Specifics(specifics_data)
            goal.specifics.breakdown = Breakdown(breakdown_data)
            goals.append(goal)
        print(goals)
        return goals

    @classmethod
    def get_all_breakdowns_before(cls, data):
        goals = []
        query = 'SELECT goal.id AS goal_id, goal.name AS goal_name, goal.description AS goal_description, goal.ispublic AS ispublic, user_has_goal.user_id AS user_id, specifics.id AS specifics_id, specifics.due_date AS specifics_duedate, specifics.due_date AS specifics_due_date, specifics.mqd AS specifics_mqd, specifics.satisfied AS specifics_satisfied, breakdown.due_date AS breakdown_due_date, why, breakdown.id AS breakdown_id, breakdown.mqd AS breakdown_mqd, breakdown.satisfied AS breakdown_satisfied FROM goal JOIN user_has_goal ON user_has_goal.goal_id = goal.id JOIN specifics ON user_has_goal.specifics_id = specifics.id JOIN breakdown ON user_has_goal.specifics_id = breakdown.specifics_id WHERE user_has_goal.user_id = %(id)s  and breakdown.due_date<CURDATE() and specifics.id=%(specid)s and goal_id =%(goal_id)s '
        print(query)
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        goals = []
        for result in results:
            goal = cls(result)
            specifics_data = {
                "goal_id": result["goal_id"],
                "user_id": result["user_id"],
                "id": result["specifics_id"],
                "due_date": result["specifics_due_date"],
                "mqd": result["specifics_mqd"],
                "satisfied": result["specifics_satisfied"],
                "why": result["why"]
            }
            breakdown_data = {
                "id": result["breakdown_id"],
                "specifics_id": result["specifics_id"],
                "due_date": result["breakdown_due_date"],
                "mqd": result["breakdown_mqd"],
                "satisfied": result["breakdown_satisfied"],
            }
            goal.specifics = Specifics(specifics_data)
            goal.specifics.breakdown = Breakdown(breakdown_data)
            goals.append(goal)
        print(goals)
        return goals
