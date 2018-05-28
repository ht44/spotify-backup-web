# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag
from spotify.app import create_app
from spotify.config import DevConfig, ProdConfig
CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)
# from spotify.database import db

#
# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.session.remove()


if __name__ == '__main__':
    app.run()
