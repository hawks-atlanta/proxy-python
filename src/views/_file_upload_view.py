import flask
from src.controllers import _file_upload_controller

views = flask.Blueprint("files", __name__)


@views.route("/file/upload", methods=["POST"])
def file_upload():
    return _file_upload_controller.upload_file_handler()
