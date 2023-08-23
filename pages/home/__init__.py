import flask
from ._view import *

home = flask.Blueprint("home", __name__)
home.register_blueprint(view)