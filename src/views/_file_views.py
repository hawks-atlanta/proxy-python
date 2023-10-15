import flask
from src.middlewares import auth_middlewares
from src.controllers.files import FILES_HANDLERS


views = flask.Blueprint("file", __name__)


@views.route("/file/<string:file_uuid>/status", methods=["GET"])
@auth_middlewares.token_required
def file_check(token, file_uuid):
    return FILES_HANDLERS["CHECK_STATE"](token, file_uuid)


@views.route("/file/<string:file_uuid>/rename", methods=["PATCH"])
@auth_middlewares.token_required
def file_rename(token, file_uuid):
    return FILES_HANDLERS["RENAME"](token, file_uuid)


@views.route("/folders", methods=["POST"])
@auth_middlewares.token_required
def dir_create(token):
    return FILES_HANDLERS["CREATE_DIRECTORY"](token)


@views.route("/file/upload", methods=["POST"])
@auth_middlewares.token_required
def file_upload(token):
    return FILES_HANDLERS["UPLOAD"](token)


@views.route("/files/list", methods=["GET"])
@auth_middlewares.token_required
def file_list(token):
    return FILES_HANDLERS["FILE_LIST"](token)
