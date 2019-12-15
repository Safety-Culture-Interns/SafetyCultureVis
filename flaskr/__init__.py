import os
import dash
from flask import Flask
from flask.helpers import get_root_path
from flaskr.backend import APISync
from flaskr import db, auth


def create_app(test_config=None):
    # create and configure the app
    server = Flask(__name__, instance_relative_config=True)
    server.config.from_mapping(
        SECRET_KEY=b'\xec\x10l\xd5\x19E&q\xc5\x85\x8c\xfc\x1a5Y\xed'
    )

    register_blueprints(server)
    register_dashapps(server)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        server.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        server.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(server.instance_path)
    except OSError:
        pass
    return server


def register_dashapps(app):
    from flaskr.dashapp1.layout import layout
    from flaskr.dashapp1.callbacks import register_callbacks

    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}
    dashapp1 = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/dashboard/',
                         assets_folder=get_root_path(__name__) + '/static/',

                         meta_tags=[meta_viewport])
    with app.app_context():
        dashapp1.title = "Dashapp 1"
        dashapp1.layout = layout
        register_callbacks(dashapp1)
        _protect_dashviews(dashapp1)


def register_blueprints(server):
    from . import auth
    from . import callbacks
    server.register_blueprint(auth.bp)
    server.register_blueprint(callbacks.bp)


# Method to protect dash views/routes
def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = auth.login_required(dashapp.server.view_functions[view_func])
