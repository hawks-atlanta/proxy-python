import flask
from src.middlewares import auth_middlewares
from src.controllers.authentication import AUTHENTICATION_HANDLERS

views = flask.Blueprint("authentication", __name__)


@views.route("/auth/login", methods=["POST"])
def auth_login():
    return AUTHENTICATION_HANDLERS["LOGIN"]()


@views.route("/auth/refresh", methods=["POST"])
@auth_middlewares.token_required
def auth_refresh(token):
    return AUTHENTICATION_HANDLERS["REFRESH"](token)
