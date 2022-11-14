from . import db


class Likes(db.Model):  # type: ignore
    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False, primary_key=True)
    track_id = db.Column(db.String(128), db.ForeignKey(
        'tracks.id'), nullable=False, primary_key=True)

##############################


class Artist(db.Model):  # type: ignore
    __tablename__ = 'artists'

    id = db.Column(db.String(128), primary_key=True, nullable=False)
    uri = db.Column(db.String(128), nullable=False, unique=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    genres = db.Column(db.ARRAY(db.String(128)), nullable=True, unique=False)
    popularity = db.Column(db.SmallInteger, nullable=False, unique=False)

    def __repr__(self):
        return self.name

##############################


class ArtistInAlbum(db.Model):  # type: ignore
    __tablename__ = 'artist_album'
    artist_id = db.Column(db.String(128), db.ForeignKey(
        'artists.id'), nullable=False, primary_key=True)
    album_id = db.Column(db.String(128), db.ForeignKey(
        'albums.id'), nullable=False, primary_key=True)


class Album(db.Model):  # type: ignore
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


class Track(db.Model):  # type: ignore
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


class Participa(db.Model):  # type: ignore
    __tablename__ = 'participa'
    track_id = db.Column(db.String(128), db.ForeignKey(
        'tracks.id'), nullable=False, primary_key=True)
    artist_id = db.Column(db.String(128), db.ForeignKey(
        'artists.id'), nullable=False, primary_key=True)

##############################


class TrackInPlaylist(db.Model):  # type: ignore
    __tablename__ = 'tracks_playlist'
    track_id = db.Column(db.String(128), db.ForeignKey(
        'tracks.id'), nullable=False, primary_key=True)
    playlist_id = db.Column(db.String(128), db.ForeignKey(
        'playlists.id'), nullable=False, primary_key=True)


class Playlist(db.Model):  # type: ignore
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
