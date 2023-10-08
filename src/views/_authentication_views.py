import flask
from src.controllers import _authentication_controllers

views = flask.Blueprint("authentication", __name__)


@views.route("/auth_login", methods=["POST"])
def auth_login():
    return _authentication_controllers.login_handler()


@views.route("/auth_refresh", methods=["POST"])
def auth_refresh():
    return _authentication_controllers.challenge()