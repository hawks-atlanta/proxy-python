import flask
from src.controllers import _authentication_controllers
from src.middlewares import auth_middlewares

views = flask.Blueprint("authentication", __name__)


@views.route("/auth_login", methods=["POST"])
def auth_login():
    return _authentication_controllers.login_handler()


@views.route("/auth_refresh", methods=["POST"])
@auth_middlewares.token_required
def auth_refresh(token):
    return _authentication_controllers.challenge_handler(token)
