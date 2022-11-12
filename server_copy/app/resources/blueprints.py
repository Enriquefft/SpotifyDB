from app.resources.user.login import login
from flask import Blueprint
from flask_restful import Api

# Blueprints
user_bp = Blueprint('users', __name__)


# API initializations
user_api = Api(user_bp)


user_api.add_resource(login, '/login')
