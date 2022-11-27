from flask_sqlalchemy import SQLAlchemy
import sqlalchemy_utils as utils
from werkzeug.security import generate_password_hash, check_password_hash

database_name="pruebauser"
database_path='postgresql://{}:{}@{}:5432/{}'.format('francko','1234', 'localhost', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app=app
    db.init_app(app)
    db.create_all()

class User(db.Model):  # type: ignore
    __tablename__ = 'users'
    # Application data
    id = db.Column(db.Integer, primary_key=True,autoincrement="auto", nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    pass_hash = db.Column(db.String(128), unique=True, nullable=False)

    #permits = db.Column(db.String(128), nullable=True,unique=False, default="READ ")
    #sp_id = db.Column(db.String(128), nullable=True, unique=True)
    #sp_uri = db.Column(db.String(128), nullable=True, unique=True)
    #sp_username = db.Column(db.String(128), nullable=True, unique=True)
    #email = db.Column(utils.EmailType(), unique=True, nullable=True)
    #refresh_token = db.Column(db.String(256), nullable=True, unique=True)
    #img_url = db.Column(db.String(256), nullable=True, unique=False)


    def get_id(self):
        return str(self.id)

    @property # propiedad password
    def password(self):
        raise AttributeError('password no definido')

    @password.setter
    def password(self,  password):
        self.pass_hash = generate_password_hash(password)

    def verificar_pass_hash(self, password):
        return check_password_hash(self.pass_hash, password)

    def __repr__(self):
        return self.username
