import flask
from src.controllers import _account_controllers

views = flask.Blueprint("account", __name__)


@views.route("/account/register", methods=["POST"])
def account_register():
    return _account_controllers.register_handler()


@views.route("/account/password", methods=["PATCH"])
def account_password():
    return _account_controllers.password_handler()
