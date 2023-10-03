import flask
from ._view import view


home = flask.Blueprint("home", __name__)
home.register_blueprint(view)
