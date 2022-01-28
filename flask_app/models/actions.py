from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.users import User
from flask_app.models.goals import Goal


class Dojo():
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
