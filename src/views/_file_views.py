import flask
from src.middlewares import auth_middlewares
from src.controllers import _file_controllers
from src.controllers import _file_upload_controller


views = flask.Blueprint("file", __name__)


@views.route("/file/<string:file_uuid>/status", methods=["GET"])
@auth_middlewares.token_required
def file_check(token, file_uuid):
    return _file_controllers.check_state_handler(token, file_uuid)


@views.route("/file/<string:file_uuid>/rename", methods=["PATCH"])
@auth_middlewares.token_required
def file_rename(token, file_uuid):
    return _file_controllers.rename_handler(token, file_uuid)


@views.route("/file/upload", methods=["POST"])
@auth_middlewares.token_required
def file_upload(token):
    return _file_upload_controller.upload_file_handler(token)
