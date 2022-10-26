from flask import Blueprint
from app.server.controllers.PermitsController import buy

permits = Blueprint('permits', __name__, template_folder="../../client/templates/permits")

permits.route("/buy", methods=["GET", "POST"]) (buy)
