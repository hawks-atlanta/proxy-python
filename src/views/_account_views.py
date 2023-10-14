import flask
from src.middlewares import auth_middlewares
from src.controllers.account import ACCOUNT_HANDLERS

views = flask.Blueprint("account", __name__)


@views.route("/account/register", methods=["POST"])
def account_register():
    return ACCOUNT_HANDLERS["REGISTER"]()


@views.route("/account/password", methods=["PATCH"])
@auth_middlewares.token_required
def account_password(token):
    return ACCOUNT_HANDLERS["UPDATE_PASSWORD"](token)
