# Flask utils
from app.models.user import User
from flask import Flask, current_app
from flask_restful import Api, Resource
from Config import devConf

from app.models import db  # , User


def create_app(config_class=devConf):

    # Jinja inline comments
    Flask.jinja_options = {'line_comment_prefix': '##'}

    app = Flask(__name__)
    app.config.from_object(config_class)

    api = Api(app)

    db.init_app(app)

    class Hello(Resource):

        def get(self):
            usr = User(username='namfijefeeffefeoiaffeaojfeafeafiefjafijafeoe',
                       pass_hash='hasefefaafeffafefeaefiaefaj_pasfeiafjaos')
            print(usr.insert())
            return {'helo': 'world'}

    api.add_resource(Hello, '/')
    # API Resources
    return app
