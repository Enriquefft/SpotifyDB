from . import db
from sqlalchemy_utils import EmailType

PERMIT_LIST = {
    #  CRUD
    "CREATE": 10,
    "READ": 0,
    "UPDATE": 15,
    "DELETE": 25
}


class User(db.Model):  # type: ignore
    __tablename__ = 'users'

    # Application data
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement="auto", nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    pass_hash = db.Column(db.String(128), unique=True, nullable=False)

    permits = db.Column(db.String(128), nullable=True,
                        unique=False, default="READ ")
    sp_id = db.Column(db.String(128), nullable=True, unique=True)
    sp_uri = db.Column(db.String(128), nullable=True, unique=True)
    sp_username = db.Column(db.String(128), nullable=True, unique=True)
    email = db.Column(EmailType(), unique=True, nullable=True)
    refresh_token = db.Column(db.String(256), nullable=True, unique=True)
    img_url = db.Column(db.String(256), nullable=True, unique=False)

    def validate_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pass_hash, password)

    def add_permit(self, permit):

        if permit not in self.permits and permit in PERMIT_LIST.keys():
            self.permits += (permit + ' ')
            self.update()
        else:
            return False

    def has_authorized(self):
        if self.sp_id and self.sp_uri and self.sp_username and self.refresh_token:
            return True
        else:
            return False

    def __repr__(self):
        return self.username

    def RefreshAccesToken(self):

        if not self.has_authorized():
            raise Exception("user is not spotify authorized")

        from flask import current_app
        CLIENT_ID = current_app.config['CLIENT_ID']
        CLIENT_SECRET = current_app.config['CLIENT_SECRET']

        request_body = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }

        from base64 import b64encode
        request_headers = {
            "Authorization": "Basic " + b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
            "Content-Type": "application/x-www-form-urlencoded"
        }

        from requests import post
        post_request = post("https://accounts.spotify.com/api/token",
                            data=request_body, headers=request_headers)

        from json import loads
        response = loads(post_request.text)

        if post_request.status_code != 200:
            raise Exception("Error")

        from flask import session
        session['access_token'] = response['access_token']
