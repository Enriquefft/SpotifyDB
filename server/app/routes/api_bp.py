from flask import Blueprint
from app.server.controllers.APIController import home as HomeController

home = Blueprint('home', __name__, template_folder=".client/templates/home")

home.route("/", methods=["GET", "POST"]) (HomeController)
#about
home.route("/about", methods=["GET"]) (about)
