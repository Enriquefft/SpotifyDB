
def GenerateState():
    from string import ascii_letters, digits
    from random import choice
    chars = ascii_letters + digits
    return ''.join(choice(chars) for _ in range(16))


def authorize():

    global STATE
    # Generate random STATE
    STATE = GenerateState()

    from .auth_consts import auth_query_parameters, SPOTIFY_AUTH_URL
    auth_query_parameters['state'] = STATE

    from urllib.parse import urlencode
    print(auth_query_parameters.get("redirect_uri"))
    url_args = urlencode(auth_query_parameters)

    auth_url = f"{SPOTIFY_AUTH_URL}/?{url_args}"

    from flask import redirect
    return redirect(auth_url)


def callback():
    from flask import request

    response_state = request.args.get('state', None)
    if response_state != STATE:
        raise Exception("State mismatch")
    if request.args.get('error') is not None:
        from flask import url_for, redirect
        return redirect(url_for('authorize'))

    # Succes
    code = request.args.get('code', None)

    from .auth_consts import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
    request_body = {
        "grant_type": "authorization_code",
        "code": str(code),
        "redirect_uri": REDIRECT_URI,
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
    authorization_header = {
        "Authorization": "Bearer {}".format(session['access_token'])}

    from .spotify_api import SPOTIFY_API_URL
    user_profile_api_endpoint = f"{SPOTIFY_API_URL}/me"
    from requests import get
    profile_response = get(user_profile_api_endpoint,
                           headers=authorization_header)
    from json import loads
    profile_data = loads(profile_response.text)

    from flask_login import current_user

    current_user.refresh_token = response['refresh_token']
    current_user.sp_id = profile_data['id']
    current_user.sp_username = profile_data['display_name']
    current_user.sp_uri = profile_data['uri']
    current_user.email = profile_data['email']
    current_user.img_url = profile_data['images'][0]['url']

    current_user.update()

    from flask import url_for, redirect
    return redirect(url_for('home.index'))
