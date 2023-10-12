import flask
from ._authentication_views import views as authentication_views
from ._account_views import views as account_views
from ._file_upload_view import views as file_upload_views


# NOTE: Register all views / routes using the following blueprint
views = flask.Blueprint("views", __name__)


views.register_blueprint(authentication_views)
views.register_blueprint(account_views)
views.register_blueprint(file_upload_views)
