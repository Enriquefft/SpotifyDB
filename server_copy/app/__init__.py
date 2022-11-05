# Flask utils
from flask import Flask


def create_app(config_class='Dev'):

    verifyConfClass(config_class)

    from app.models import db

    # Jinja inline comments
    Flask.jinja_options = {'line_comment_prefix': '##'}

    app = Flask(__name__)
    app.config.from_object(f'app.Config.{config_class}Config')

    db.init_app(app)

    # Blueprints
    from app.resources.blueprints import user_bp
    app.register_blueprint(user_bp)

    return app


# Move to utils.py?
def verifyConfClass(config_class):
    options = ['Dev', 'Prod']
    if config_class not in options:

        from click import BadParameter
        from sys import exit

        BadParameter(
            f"\n'{config_class}' config setup not available.\nAvailable options are:\n{[x for x in options]}").show()
        exit()
