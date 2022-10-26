def index():

    from flask_login import current_user

    if not current_user.is_authenticated:
        from flask import redirect, url_for
        return redirect(url_for('users.login'))
    elif not current_user.has_authorized():
        from flask import redirect, url_for
        return redirect(url_for('users.authorize'))
        
    from .spotify_api import SPOTIFY_API_URL, GenerateHeader

    from requests import get

    featured_playlists = get(f"{SPOTIFY_API_URL}/browse/featured-playlists", headers=GenerateHeader())
    user_playlists = get(f"{SPOTIFY_API_URL}/me/playlists", headers=GenerateHeader())

    data = featured_playlists.json()
    featured_playlists = [ { 'image' : playlist['images'][0]['url'], 'name' : playlist['name'], 'link' : playlist['external_urls']['spotify'] } for playlist in data['playlists']['items'] ]

    data = user_playlists.json()
    user_playlists = [ { 'image' : playlist['images'][0]['url'], 'name' : playlist['name'], 'link' : playlist['external_urls']['spotify'] } for playlist in data['items'] ]

    from flask import render_template
    return render_template("home.html", featured_playlists=featured_playlists, user_playlists=user_playlists)
