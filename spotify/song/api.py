# -*- coding: utf-8 -*-
"""Song api."""
from flask import Blueprint, request, jsonify
from sqlalchemy import exc
from .model import Song
from .access import SongAccess
from spotify.database import db


blueprint = Blueprint('song', __name__, url_prefix='/songs')


@blueprint.route('/', methods=['GET', 'POST'])
def songs():
    if request.method == 'GET':
        song_access = SongAccess(Song, db.session)
        name = request.args.get('name')
        try:
            if name:
                records = song_access.search(name=name)
            else:
                records = song_access.list()
            return jsonify([r.dict for r in records])
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)
    elif request.method == 'POST':
        song_access = SongAccess(Song, db.session)
        try:
            record = song_access.insert(album_id=request.form['album_id'],
                                        name=request.form['name'])
            return jsonify(record.dict)
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)


@blueprint.route('/<song_id>', methods=['GET', 'DELETE'])
def song(song_id):
    if request.method == 'GET':
        song_access = SongAccess(Song, db.session)
        try:
            record = song_access.get(record_id=song_id)
            return jsonify(record.dict)
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)
    elif request.method == 'DELETE':
        song_access = SongAccess(Song, db.session)
        try:
            record = song_access.delete(record_id=song_id)
            return jsonify(record.id)
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)