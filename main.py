import flask
from src.views import views

app = flask.Flask(__name__)
app.register_blueprint(views)

if __name__ == "__main__":
    app.run(debug=True)
