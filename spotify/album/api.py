# -*- coding: utf-8 -*-
"""Album api."""
from flask import Blueprint, request, jsonify
from sqlalchemy import exc
from . import model
from spotify.database import db


blueprint = Blueprint('album', __name__, url_prefix='/albums')


@blueprint.route('/', methods=['GET', 'POST'])
def get_albums():
    if request.method == 'GET':
        album = model.Album()
        records = album.query.all()
        j = [r.dict for r in records]
        return jsonify(j)
    elif request.method == 'POST':
        album = model.Album(artist_id=request.form['artist_id'],
                            name=request.form['name'])
        try:
            db.session.add(album)
            db.session.commit()
            return jsonify(album.dict)
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            db.session.flush()
            message = e.orig.args
            return jsonify(message)


@blueprint.route('/<album_id>', methods=['GET', 'DELETE'])
def get_artist(album_id):
    if request.method == 'GET':
        album = model.Album()
        try:
            record = album.query.filter_by(id=album_id).first()
            if record is None:
                return jsonify('not found')
            return jsonify(record.dict)
        except exc.SQLAlchemyError as e:
            message = e.args
            return jsonify(message)
    elif request.method == 'DELETE':
        try:
            album = model.Album()
            record = album.query.filter_by(id=album_id).first()
            if record is None:
                return jsonify('not found')
            db.session.delete(record)
            db.session.commit()
            return jsonify(record.id)
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            db.session.flush()
            message = e.args
            return jsonify(message)


@blueprint.route('/<album_id>/songs', methods=['GET'])
def get_album_songs(album_id):
    if request.method == 'GET':
        album = model.Album()
        record = album.query.filter_by(id=album_id).first()
        return jsonify(record.songs_dict)
