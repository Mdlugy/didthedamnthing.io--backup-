from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_regex = re.compile(
    r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*])[\w\d!@#$%^&*]{6,60}$")
name_regex = re.compile(r'^[A-Za-z]{2,20}$')
username_regex = re.compile(r'^[a-z0-9A-Z_@!#$%^&*]{6,20}$')


class User:
    def __init__(self, data):
        self.id = data["id"]
        if "password" in data:
            self.password = data['password']
            self.created_at = data['created_at']
            self.updated_at = data['updated_at']
            self.username = data["username"]
            self.email = data['email']

        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.name = f"{self.first_name}, {self.last_name}"

    @staticmethod
    def validate_input(data):
        is_valid = True
        print(data['pw_hash'])
        print(data['email'])
        # test whether a field matches the pattern
        if not email_regex.match(data['email']):
            flash("Invalid email address!", "register")
            is_valid = False
        if not name_regex.match(data['first_name']):
            flash(
                "Please enter a valid first name.", "register")
            is_valid = False
        if not name_regex.match(data['last_name']):
            flash(
                "Please enter a valid last name.", "register")
            is_valid = False
        if not username_regex.match(data['username']):
            flash(
                "Please enter a username at least 6 characters", "register")
            is_valid = False
        if not password_regex.match(data['pw_hash']):
            flash("Please use a password at least 8 characters with at least 1 capital letter, 1 number and one special character", "register")
            is_valid = False
        if data['pw_hash'] != data['confirm']:
            flash("Please make sure your passwords match", "register")
            is_valid = False

        return is_valid

    @classmethod
    def register(cls, data):
        if User.checkUsername(data) == False:
            return
        if User.checkEmail(data) == False:
            return
        query = "INSERT INTO user (first_name,last_name,email,username,pw_hash,created_at,updated_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(username)s,%(pw_hash)s,NOW(),NOW());"
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        flash("registration sucessfull", "register")
        print(results)
        return results

    @classmethod
    def checkUsername(cls, data):
        query = "Select id from user where username=%(username)s"
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        if len(results) == 0:
            return True
        flash("username already exists", "register")
        return False

    @classmethod
    def checkEmail(cls, data):

        query = "Select id from user where email=%(email)s"
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        if len(results) == 0:
            return True
        flash("email already exists", "register")
        return False

    @classmethod
    def checkUser(cls, data):
        if username_regex.match(data['userToken']):
            query = "Select pw_hash from user where username=%(userToken)s"
        elif email_regex.match(data['userToken']):
            query = "Select pw_hash from user where email=%(userToken)s"
        else:
            flash("please enter valid Username or email", "login")
            return False

        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)
        print(results)
        if len(results) == 0:
            if username_regex.match(data['userToken']):
                flash("username not found", "login")
                return False
            else:
                flash("email not found", "login")
                return False
        return results[0]["pw_hash"]

    @classmethod
    def getuserinfo(cls, data):
        if username_regex.match(data['userToken']):
            query = "Select * from user where username=%(userToken)s"
        elif email_regex.match(data['userToken']):
            query = "Select * from user where email=%(userToken)s"
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)[0]
        return results

    @classmethod
    def getuserinfobyid(cls, data):
        query = "Select * from user where id=%(id)s"
        connection = connectToMySQL('didthedamnthing')
        results = connection.query_db(query, data)[0]
        return results
