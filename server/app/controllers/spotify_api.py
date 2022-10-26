SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = f"{SPOTIFY_API_BASE_URL}/{API_VERSION}"

def GenerateHeader():
    from flask import session
    from flask_login import current_user
    current_user.RefreshAccesToken()
    authorization_header = {"Authorization": "Bearer {}".format(session['access_token'])}
    return authorization_header
