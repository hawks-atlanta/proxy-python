import flask
from src.middlewares import auth_middlewares
from src.controllers import _account_controllers

views = flask.Blueprint("account", __name__)


@views.route("/account/register", methods=["POST"])
def account_register():
    return _account_controllers.register_handler()


@views.route("/account/password", methods=["PATCH"])
@auth_middlewares.token_required
def account_password(token):
    return _account_controllers.update_password_handler(token)
