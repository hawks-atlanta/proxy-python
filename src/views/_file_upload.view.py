import flask
from src.controllers import _file_upload_controller

views = flask.Blueprint("account", __name__)


@views.route("/file/upload", methods=["PATCH"])
def file_upload():
    return _file_upload_controller.upload_file_handler()
