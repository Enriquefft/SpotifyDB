from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

import sqlalchemy_utils as utils


db = SQLAlchemy()


class ModelParent:

    id = 0

    def insert(self):
        error = False

        id = None

        try:
            db.session.add(self)
            db.session.commit()
            id = self.id
        except Exception as e:
            print('error: ', e)
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        print("insert:")
        print('id: ', id)
        print()
        return id, error

    def format(self):
        dic = vars(self)
        dic.pop('pass_hash', None)
        return dic

    def update(self):
        error = False

        print("UPDATE:")
        print(self.format())
        print()
        try:
            db.session.commit()
        except Exception as e:
            print('error: ', e)
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        return self, error

    def delete(self):
        error = False
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print('error: ', e)
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        return error


PERMIT_LIST = {
    #  CRUDS
    "CREATE": 10,
    "READ": 0,
    "UPDATE": 15,
    "DELETE": 25
}


class User(db.Model, UserMixin, ModelParent):  # type: ignore
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
    email = db.Column(utils.EmailType(), unique=True, nullable=True)
    refresh_token = db.Column(db.String(256), nullable=True, unique=True)
    img_url = db.Column(db.String(256), nullable=True, unique=False)

    def add_permit(self, permit):

        if (permit + ' ') not in self.permits and permit in PERMIT_LIST.keys():
            self.permits += (permit + ' ')
            self.update()
        else:
            assert False, "Error"

    def get_id(self):
        return str(self.id)

    def has_authorized(self):
        if self.sp_id and self.sp_uri and self.sp_username and self.refresh_token:
            return True
        else:
            return False

    def __repr__(self):
        return self.username

    def RefreshAccesToken(self):

        if not self.has_authorized() or not self.is_active:
            exit()

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
            pass

        from flask import session
        session['access_token'] = response['access_token']


class Likes(db.Model, ModelParent):  # type: ignore
    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False, primary_key=True)
    track_id = db.Column(db.String(128), db.ForeignKey(
        'tracks.id'), nullable=False, primary_key=True)

##############################


class Artist(db.Model, ModelParent):  # type: ignore
    __tablename__ = 'artists'

    id = db.Column(db.String(128), primary_key=True, nullable=False)
    uri = db.Column(db.String(128), nullable=False, unique=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    genres = db.Column(db.ARRAY(db.String(128)), nullable=True, unique=False)
    popularity = db.Column(db.SmallInteger, nullable=False, unique=False)

    def __repr__(self):
        return self.name

##############################


class ArtistInAlbum(db.Model, ModelParent):  # type: ignore
    __tablename__ = 'artist_album'
    artist_id = db.Column(db.String(128), db.ForeignKey(
        'artists.id'), nullable=False, primary_key=True)
    album_id = db.Column(db.String(128), db.ForeignKey(
        'albums.id'), nullable=False, primary_key=True)


class Album(db.Model, ModelParent):  # type: ignore
    __tablename__ = 'albums'
    id = db.Column(db.String(128), primary_key=True, nullable=False)
    uri = db.Column(db.String(128), nullable=False, unique=True)
    track_count = db.Column(
        db.SmallInteger, nullable=False, unique=False, default=1)
    type = db.Column(db.String(11), nullable=False, unique=False)
    name = db.Column(db.String(128), nullable=False, unique=False)
    participa = db.relationship(
        'Artist', secondary='artist_album', backref='artistas')

    def __repr__(self):
        return self.name

##############################


class Track(db.Model, ModelParent):  # type: ignore
    __tablename__ = 'tracks'
    id = db.Column(db.String(128), primary_key=True, nullable=False)
    uri = db.Column(db.String(128), nullable=False, unique=True)
    popularity = db.Column(db.SmallInteger, nullable=False, unique=False)
    is_explicit = db.Column(db.Boolean, default=False, nullable=False)
    duration = db.Column(db.SmallInteger, nullable=False, unique=False)
    name = db.Column(db.String(128), nullable=False, unique=False)
    disc_number = db.Column(
        db.SmallInteger, nullable=False, unique=False, default=1)
    album_of = db.Column(db.String(128), db.ForeignKey(
        'albums.id'), nullable=False, unique=False)
    participa = db.relationship(
        'Artist', secondary='participa', backref='tracks')

    def __repr__(self):
        return self.name


class Participa(db.Model, ModelParent):  # type: ignore
    __tablename__ = 'participa'
    track_id = db.Column(db.String(128), db.ForeignKey(
        'tracks.id'), nullable=False, primary_key=True)
    artist_id = db.Column(db.String(128), db.ForeignKey(
        'artists.id'), nullable=False, primary_key=True)

##############################


class TrackInPlaylist(db.Model, ModelParent):  # type: ignore
    __tablename__ = 'tracks_playlist'
    track_id = db.Column(db.String(128), db.ForeignKey(
        'tracks.id'), nullable=False, primary_key=True)
    playlist_id = db.Column(db.String(128), db.ForeignKey(
        'playlists.id'), nullable=False, primary_key=True)


class Playlist(db.Model, ModelParent):  # type: ignore
    __tablename__ = 'playlists'
    id = db.Column(db.String(128), primary_key=True, nullable=False)
    uri = db.Column(db.String(128), nullable=False, unique=True)
    name = db.Column(db.String(128), nullable=False)
    is_public = db.Column(db.Boolean, default=True)
    dueño = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    tracks = db.relationship(
        'Track', secondary='tracks_playlist', backref='tracks')

    def __repr__(self):
        return self.name
