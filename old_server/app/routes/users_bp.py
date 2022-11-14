from flask import Blueprint
from app.server.controllers.LoginController import login
from app.server.controllers.RegisterController import register
from app.server.controllers.AuthorizeController import authorize, callback

users = Blueprint('users', __name__, template_folder="../../client/templates/users")

users.route("/login", methods=["GET", "POST"]) (login)
users.route("/register", methods=["GET", "POST"]) (register)
users.route("/authorize", methods=["GET"]) (authorize)
users.route("/callback", methods=["GET"]) (callback)
