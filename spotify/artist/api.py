# -*- coding: utf-8 -*-
"""Artist api."""
from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from . import model
from spotify.database import db

blueprint = Blueprint('artist', __name__, url_prefix='/artists')


@blueprint.route('/', methods=['GET', 'POST'])
def get_artists():
    if request.method == 'GET':
        artist = model.Artist()
        records = artist.query.all()
        j = [r.serialize for r in records]
        return jsonify(j)

    elif request.method == 'POST':
        artist = model.Artist(name=request.form['name'])
        try:
            db.session.add(artist)
            db.session.commit()
            return jsonify(artist.serialize)
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            db.session.flush()
            message = e.orig.args
            return jsonify(message)


@blueprint.route('/<artist_id>', methods=['GET', 'DELETE'])
def get_artist(artist_id):
    if request.method == 'GET':
        artist = model.Artist()
        try:
            record = artist.query.filter_by(id=artist_id).first()
            if record is None:
                return jsonify('not found')
            return jsonify(record.serialize)
        except exc.SQLAlchemyError as e:
            message = e.args
            return jsonify(message)
    elif request.method == 'DELETE':
        try:
            artist = model.Artist()
            record = artist.query.filter_by(id=artist_id).first()
            db.session.delete(record)
            db.session.commit()
            return jsonify(record.serialize)
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            db.session.flush()
            message = e.args
            return jsonify(message)