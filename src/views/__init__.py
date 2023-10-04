import flask
from ._authentication_views import views as authentication_views


# NOTE: Register all views / routes using the following blueprint
views = flask.Blueprint("views", __name__)


views.register_blueprint(authentication_views)
