import flask

view = flask.Blueprint("home", __name__)

@view.route("/", methods=["GET"])
def index():
    return flask.render_template("index.html")