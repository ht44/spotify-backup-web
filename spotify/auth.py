from spotify import app
from flask import redirect, request, jsonify
from urllib.parse import urlencode
from base64 import b64encode
import requests
from spotify.constants import TOKEN_ENDPOINT, REDIRECT_URI
from os import environ


@app.route('/login')
def login():
    params = (
        ('client_id', environ['CLIENT_ID']),
        ('response_type', 'code'),
        ('redirect_uri', 'http://localhost:5000/callback'),
        ('scope', 'user-library-read'),
        ('show_dialog', 'true')
    )
    urlencode(params)
    url = 'https://accounts.spotify.com/authorize/' + '?' + urlencode(params)
    return redirect(url, code=302)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': environ['CLIENT_ID'],
        'client_secret': environ['CLIENT_SECRET']
    }
    r = requests.post(TOKEN_ENDPOINT, data=payload)
    j = r.json()
    if 'error' in j:
        return jsonify(j)
    environ['SPOTIFY_ACCESS_TOKEN'] = j['access_token']
    environ['SPOTIFY_REFRESH_TOKEN'] = j['refresh_token']
    return jsonify(j)


@app.route('/refresh')
def refresh():
    creds = bytes(environ['CLIENT_ID'] + ':' + environ['CLIENT_SECRET'], encoding='utf-8')
    b64creds = b64encode(creds).decode('ascii')
    headers = {'Authorization': 'Basic %s' % b64creds}
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': environ['SPOTIFY_REFRESH_TOKEN'],
    }
    r = requests.post(TOKEN_ENDPOINT, data=payload, headers=headers)
    j = r.json()
    if 'error' in j:
        return jsonify(j)
    environ['SPOTIFY_ACCESS_TOKEN'] = j['access_token']
    return jsonify(j)