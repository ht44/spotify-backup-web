# -*- coding: utf-8 -*-
"""Song api."""
from flask import Blueprint, request, jsonify
from sqlalchemy import exc
from . import model
from spotify.database import db

blueprint = Blueprint('song', __name__, url_prefix='/songs')


@blueprint.route('/', methods=['GET', 'POST'])
def get_songs():
    if request.method == 'GET':
        song = model.Song()
        records = song.query.all()
        j = [r.dict for r in records]
        return jsonify(j)
    elif request.method == 'POST':
        song = model.Song(album_id=request.form['album_id'],
                          name=request.form['name'])
        try:
            db.session.add(song)
            db.session.commit()
            return jsonify(song.dict)
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            db.session.flush()
            message = e.args
            return jsonify(message)


@blueprint.route('/<song_id>', methods=['GET', 'DELETE'])
def get_artist(song_id):
    if request.method == 'GET':
        song = model.Song()
        try:
            record = song.query.filter_by(id=song_id).first()
            if record is None:
                return jsonify('not found')
            return jsonify(record.dict)
        except exc.SQLAlchemyError as e:
            message = e.args
            return jsonify(message)
    elif request.method == 'DELETE':
        try:
            song = model.Song()
            record = song.query.filter_by(id=song_id).first()
            if record is  None:
                return jsonify('not found')
            db.session.delete(record)
            db.session.commit()
            return jsonify(record.id)
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            db.session.flush()
            message = e.args
            return jsonify(message)