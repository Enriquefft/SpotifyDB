from flask_restful import Resource
from flask import Blueprint
from flask_restful import Api

# Blueprints
user_bp = Blueprint('users', __name__)


# API initializations
user_api = Api(user_bp)

#from resources.controllers.login import login


class login(Resource):
    def get(self):
        return {'task': 'user_loged in'}


user_api.add_resource(login, '/')
