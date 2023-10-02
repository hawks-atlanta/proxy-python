import flask
from ._view import view

def bad_function(): 
        a = 1
        b  =2 
        return b







home = flask.Blueprint("home", __name__)
home.register_blueprint(view)
