# -*- coding: utf-8 -*-
"""Spotify api."""
from flask import Blueprint, jsonify, redirect, request, current_app as app
from spotify.constants import USER_LIB_ENDPOINT
from spotify.spotify.model import SpotifyLibrary, SpotifyTrack
from urllib.parse import urlencode
from base64 import b64encode
import requests
from spotify.constants import TOKEN_ENDPOINT, REDIRECT_URI, LOGIN_ENDPOINT

blueprint = Blueprint('spotify', __name__, url_prefix='/spotify')

@blueprint.route('/')
def songs():
    """List albums."""
    return 'spotify'


@blueprint.route('/login')
def login():
    params = (
        ('client_id', app.config['CLIENT_ID']),
        ('response_type', 'code'),
        ('redirect_uri', REDIRECT_URI),
        ('scope', 'user-library-read'),
        ('show_dialog', 'true')
    )
    urlencode(params)
    url = LOGIN_ENDPOINT + '?' + urlencode(params)
    return redirect(url, code=302)


@blueprint.route('/callback')
def callback():
    code = request.args.get('code')
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': app.config['CLIENT_ID'],
        'client_secret': app.config['CLIENT_SECRET']
    }
    r = requests.post(TOKEN_ENDPOINT, data=payload)
    j = r.json()
    if 'error' in j:
        return jsonify(j)
    app.config['SPOTIFY_ACCESS_TOKEN'] = j['access_token']
    app.config['SPOTIFY_REFRESH_TOKEN'] = j['refresh_token']
    return jsonify(j)


@blueprint.route('/refresh')
def refresh():
    creds = bytes(app.config['CLIENT_ID'] + ':' + app.config['CLIENT_SECRET'], encoding='utf-8')
    b64creds = b64encode(creds).decode('ascii')
    headers = {'Authorization': 'Basic %s' % b64creds}
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': app.config['SPOTIFY_REFRESH_TOKEN'],
    }
    r = requests.post(TOKEN_ENDPOINT, data=payload, headers=headers)
    j = r.json()
    if 'error' in j:
        return jsonify(j)
    app.config['SPOTIFY_ACCESS_TOKEN'] = j['access_token']
    return jsonify(j)


@blueprint.route('/tracks')
def get_tracks():
    auth_header = 'Authorization: Bearer {}'.format(app.config['SPOTIFY_ACCESS_TOKEN'])
    headers = {'Authorization': auth_header}
    r = requests.get(USER_LIB_ENDPOINT + '?limit=50', headers=headers)
    j = r.json()
    return jsonify(j)


@blueprint.route('/llibrary')
def get_librarys():

    auth_header = 'Authorization: Bearer {}'.format(app.config['SPOTIFY_ACCESS_TOKEN'])
    headers = {'Authorization': auth_header}
    r = requests.get('https://api.spotify.com/v1/me/tracks?limit=50', headers=headers)
    j = r.json()
    if 'error' in j:
        return jsonify(j)

    result = j['items']
    while j['next']:
        r = requests.get(j['next'], headers=headers)
        j = r.json()
        if 'error' in j:
            return jsonify(j)
        result = result + j['items']

    tracks = [SpotifyTrack(t) for t in result]
    library = SpotifyLibrary(tracks)
    return jsonify(library.to_list())

    # spotify_tracks = [SpotifyTrack(t) for t in result]
    #
    # with open('all.json') as data_file:
    #     data = json.load(data_file)
    #     tracks = [SpotifyTrack(t) for t in data]
    #     library = SpotifyLibrary(tracks)
    #     return jsonify(library.to_list())
