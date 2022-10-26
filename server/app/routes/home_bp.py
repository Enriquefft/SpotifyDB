from flask import Blueprint
from app.server.controllers.HomeController import index
from app.server.controllers.AboutController import about

home = Blueprint('home', __name__, template_folder="../../client/templates/home")

home.route("/", methods=["GET", "POST"]) (index)
#about
home.route("/about", methods=["GET"]) (about)
