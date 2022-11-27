from flask import (
    Flask,
    abort,
    jsonify,
    request,
)

import jwt
from flask_cors import CORS
from models import setup_db, User


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'datasecret'
    setup_db(app)
    CORS(app, origins=['http://127.0.0.1:8080', 'http://localhost:8080'], max_age=10)
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'OPTIONS, GET, POST, PATCH, PUT, DELETE')
        response.headers.add('Access-Control-Max-Age', 10)
        return response

    @app.route('/register', methods=['POST'])
    def register():
            body = request.get_json()
            name = body.get('name', None)
            username = body.get('username', None)
            password = body.get('password', None)

            if name is None or username is None or password is None:
                abort(422)

            #Search
            db_user = User.query.filter(User.username==username).first()
            errors_to_send = []
            if db_user is not None:
                if db_user.username == username:
                    errors_to_send.append('ya existe la cuenta')

                if len(password) < 4:
                    errors_to_send.append('la contrasenia tiene que tener mayor a 4 caracteres')

                if len(errors_to_send) > 0:
                    return jsonify({
                        'success': False,
                        'code': 422,
                        'messages': errors_to_send
                    }), 422

            user = User(name=name, username=username, password=password)
            id_user_new = user.insert()

            token = jwt.encode({
                'id': id_user_new,
            }, app.config['SECRET_KEY'])

            return  jsonify({'success':True, 'token':str(token),'user_id':id_user_new})

    @app.route('/login', methods=['POST'])
    def login():
        body = request.get_json()
        username = body.get('username', None)
        password = body.get('password', None)

        user = User.query.filter(User.username==username).one_or_none()
        is_logged = user is not None and user.verify_password(password)
        if not is_logged:
            abort(401)
        else:
            token = jwt.encode({
                'id': str(user.get_id()),
            }, app.config['SECRET_KEY'])
            return jsonify({
                'success': True,
                'token': token,
                'user_id': user.get_id(),
                'name': user.username
            })