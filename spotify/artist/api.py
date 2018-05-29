# -*- coding: utf-8 -*-
"""Artist api."""
from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from .model import Artist
from .access import ArtistAccess
from spotify.database import db


blueprint = Blueprint('artist', __name__, url_prefix='/artists')


@blueprint.route('/', methods=['GET', 'POST'])
def artists():
    if request.method == 'GET':
        access = ArtistAccess(Artist, db.session)
        name = request.args.get('name')
        try:
            if name is not None:
                records = access.search(name=name)
            else:
                records = access.list()
            return jsonify([r.dict for r in records])
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)
    elif request.method == 'POST':
        access = ArtistAccess(Artist, db.session)
        try:
            record = access.insert(name=request.form['name'])
            return jsonify(record.dict)
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)


@blueprint.route('/<artist_id>', methods=['GET', 'DELETE'])
def artist(artist_id):
    if request.method == 'GET':
        access = ArtistAccess(Artist, db.session)
        try:
            record = access.get(record_id=artist_id)
            return jsonify(record.dict)
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)
    elif request.method == 'DELETE':
        access = ArtistAccess(Artist, db.session)
        try:
            record = access.delete(record_id=artist_id)
            return jsonify(record.dict)
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)


@blueprint.route('/<artist_id>/albums', methods=['GET'])
def albums(artist_id):
    if request.method == 'GET':
        access = ArtistAccess(Artist, db.session)
        try:
            record = access.get(record_id=artist_id)
            return jsonify([r.dict for r in record.albums])
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)


@blueprint.route('/<artist_id>/songs', methods=['GET'])
def songs(artist_id):
    if request.method == 'GET':
        access = ArtistAccess(Artist, db.session)
        try:
            record = access.get(record_id=artist_id)
            return jsonify(record.songs_dict)
        except exc.SQLAlchemyError as e:
            return jsonify(e.args)
