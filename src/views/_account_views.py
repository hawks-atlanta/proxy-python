import flask
from src.controllers import _account_controllers

views = flask.Blueprint("account", __name__)


@views.route("/account_register", methods=["POST"])
def account_register():
    return _account_controllers.register_handler()
