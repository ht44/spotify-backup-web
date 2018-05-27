from spotify import app
import requests
from flask import jsonify
from spotify.constants import USER_LIB_ENDPOINT
from os import environ
import json
from spotify.models.SpotifyLibrary import SpotifyLibrary
from spotify.models.SpotifyTrack import SpotifyTrack
import inspect

@app.route('/tracks')
def get_tracks():
    auth_header = 'Authorization: Bearer {}'.format(environ['SPOTIFY_ACCESS_TOKEN'])
    headers = {'Authorization': auth_header}
    r = requests.get(USER_LIB_ENDPOINT + '?limit=50', headers=headers)
    j = r.json()
    return jsonify(j)


@app.route('/alltracks')
def get_all_tracks():

    auth_header = 'Authorization: Bearer {}'.format(environ['SPOTIFY_ACCESS_TOKEN'])
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
