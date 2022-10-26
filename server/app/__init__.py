# Flask utils
from flask import Flask, current_app

def create_app(config_class='DevConfig'):

    Flask.jinja_options = {'line_comment_prefix': '##'} # Jinja inline comments

    app = Flask(__name__, template_folder="./client/templates", static_folder="./client/static")
    app.config.from_object('.Config.' + config_class)
    #app.config.from_object('Config.ProdConfig')

    # Initialize Plugins
    from app.server.models import db

    from flask_cors import CORS
    from flask_migrate import Migrate

    migrate = Migrate()
    cors = CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Register blueprints
    from app.server.routes.users_bp import users
    from app.server.routes.home_bp import home
    from app.server.routes.permits_bp import permits

    app.register_blueprint(users)
    app.register_blueprint(home)
    app.register_blueprint(permits)

    @login_manager.user_loader
    def load_user(user_id):
        from app.server.models import User
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

    import logging
    #logging.info("\n\nNew user")
    #logging.basicConfig(filename="sqllogs.txt", filemode="w")
    #logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)



    return app

