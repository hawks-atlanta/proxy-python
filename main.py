import flask
from flask_cors import CORS
from src.views import views

app = flask.Flask(__name__)
app.register_blueprint(views)
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    app.run(debug=True)
