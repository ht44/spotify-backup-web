# -*- coding: utf-8 -*-
"""Album api."""
from flask import Blueprint, request, jsonify
from sqlalchemy import exc
from .model import Album
from .access import AlbumAccess
from spotify.database import db


blueprint = Blueprint('album', __name__, url_prefix='/albums')


@blueprint.route('/', methods=['GET', 'POST'])
def albums():
    if request.method == 'GET':
        album_access = AlbumAccess(Album, db.session)
        name = request.args.get('name')
        try:
            if name:
                records = album_access.search(name=name)
            else:
                records = album_access.list()
            return jsonify([r.dict for r in records])
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)
    elif request.method == 'POST':
        album_access = AlbumAccess(Album, db.session)
        try:
            record = album_access.insert(artist_id=request.form['artist_id'],
                                         name=request.form['name'])
            return jsonify(record.dict)
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)


@blueprint.route('/<album_id>', methods=['GET', 'DELETE'])
def album(album_id):
    if request.method == 'GET':
        album_access = AlbumAccess(Album, db.session)
        try:
            record = album_access.get(record_id=album_id)
            return jsonify(record.dict)
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)
    elif request.method == 'DELETE':
        album_access = AlbumAccess(Album, db.session)
        try:
            record = album_access.delete(record_id=album_id)
            return jsonify(record.id)
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)


@blueprint.route('/<album_id>/songs', methods=['GET'])
def get_album_songs(album_id):
    if request.method == 'GET':
        album_access = AlbumAccess(Album, db.session)
        try:
            record = album_access.get(record_id=album_id)
            return jsonify(record.songs_dict)
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)
