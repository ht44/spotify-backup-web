# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

from spotify import song, album, artist, spotify
from spotify.extensions import db
from spotify.config import ProdConfig
from flask_migrate import Migrate

# from {{spotify-backup.app_name}} import commands, public, user
# from {{cookiecutter.app_name}}.extensions import bcrypt, cache, csrf_protect, db, debug_toolbar, login_manager, migrate, webpack
# from {{cookiecutter.app_name}}.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    # register_errorhandlers(app)
    register_shellcontext(app)
    # register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate = Migrate(app, db)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(song.api.blueprint)
    app.register_blueprint(album.api.blueprint)
    app.register_blueprint(artist.api.blueprint)
    app.register_blueprint(spotify.api.blueprint)
    return None


# def register_errorhandlers(app):
#     """Register error handlers."""
#     def render_error(error):
#         """Render error template."""
#         # If a HTTPException, pull the `code` attribute; default to 500
#         error_code = getattr(error, 'code', 500)
#         return render_template('{0}.html'.format(error_code)), error_code
#     for errcode in [401, 404, 500]:
#         app.errorhandler(errcode)(render_error)
#     return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'Song': song.model.Song,
            'Album': album.model.Album,
            'Artist': artist.model.Artist}
    app.shell_context_processor(shell_context)


# def register_commands(app):
#     """Register Click commands."""
#     app.cli.add_command(commands.test)
#     app.cli.add_command(commands.lint)
#     app.cli.add_command(commands.clean)
#     app.cli.add_command(commands.urls)
