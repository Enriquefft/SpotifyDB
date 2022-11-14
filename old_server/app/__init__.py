# Flask utils
from flask import Flask, current_app
from ..Config import devConf


def create_app(config_class=devConf):

    # Jinja inline comments
    Flask.jinja_options = {'line_comment_prefix': '##'}

    app = Flask(__name__, template_folder="./client/templates",
                static_folder="./client/static")

    app.config.from_object(config_class)
    # app.config.from_object('Config.ProdConfig')

    # Initialize Plugins
    from app import models

    from flask_cors import CORS
    from flask_migrate import Migrate

    migrate = Migrate()
    cors = CORS(app)

    models.db.init_app(app)
    migrate.init_app(app, models.db)

    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Register blueprints
    from app.routes.users_bp import users
    from app.routes.home_bp import home
    from app.routes.permits_bp import permits

    app.register_blueprint(users)
    app.register_blueprint(home)
    app.register_blueprint(permits)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    from functools import wraps
    from flask_login import current_user

    def permits_requiered(permits):
        def wrapper(fn):
            @wraps(fn)
            def decorated_view(*args, **kwargs):
                if not current_user.is_authenticated():
                    return login_manager.unauthorized()

                requiered_permits = permits.split()
                user_permits = current_user.permits.split()
                if not all(perm in user_permits for perm in requiered_permits):
                    return login_manager.unauthorized()

                return fn(*args, **kwargs)
            return decorated_view
        return wrapper

    return app
