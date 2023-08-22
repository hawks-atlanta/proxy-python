import flask
import pages.home

app = flask.Flask(__name__, template_folder="templates")

app.register_blueprint(pages.home.home)
