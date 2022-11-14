from app.resources.user.login import login
from app.resources.home.home import home
from flask import Blueprint
from flask_restful import Api

# Blueprints
user_bp = Blueprint('users', __name__)
home_bp = Blueprint('home', __name__)


# API initializations
user_api = Api(user_bp)
home_api = Api(home_bp)


user_api.add_resource(login, '/login')
home_api.add_resource(home, '/')
