# -*- coding: utf-8 -*-
"""Spotify api."""
from pprint import pprint

from flask import Blueprint, jsonify, redirect, request, current_app as app
from spotify.spotify.model import SpotifyLibrary, SpotifyTrack
from urllib.parse import urlencode
from base64 import b64encode
import requests
from spotify.constants import TOKEN_ENDPOINT, REDIRECT_URI, LOGIN_ENDPOINT
from spotify.song.model import Song
from spotify.album.model import Album
from spotify.artist.model import Artist
from spotify.database import db
from spotify.utils.models import get_or_create


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


@blueprint.route('/library')
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

    # with open('all.json') as data_file:
    #     result = json.load(data_file)

    tracks = [SpotifyTrack(t) for t in result]
    library = SpotifyLibrary(tracks).normalize()

    for key, value in library.items():
        a = get_or_create(db.session, Artist, name=key)
        for k, v in value['albums'].items():
            alb = get_or_create(db.session, Album, name=k, artist_id=a.id)
            for s in v['songs']:
                son = get_or_create(db.session, Song, name=s, album_id=alb.id)
    return jsonify(library)
