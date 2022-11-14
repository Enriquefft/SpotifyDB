from flask import current_app
# Client Keys
CLIENT_ID = current_app.config['CLIENT_ID']
CLIENT_SECRET = current_app.config['CLIENT_SECRET']

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"


# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000

REDIRECT_URI = "{}:{}/callback".format(CLIENT_SIDE_URL, PORT)

# SCOPE
SCOPE  = (  "playlist-read-private"
            " playlist-read-collaborative"
            " user-library-modify"
            " playlist-modify-private"
            " playlist-modify-public"
            " user-read-email"
            " user-top-read"
            " user-read-recently-played"
            " user-read-private"
            " user-library-read"
         )

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "show_dialog": 'false',
    "client_id": CLIENT_ID
}

