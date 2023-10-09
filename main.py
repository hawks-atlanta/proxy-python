import flask
from flask_cors import CORS
from src.views import views
from src.config.environment import variables

app = flask.Flask(__name__)
app.register_blueprint(views)

allowed_origins_list = variables["ALLOWED_ORIGINS"].split(",")

CORS(app, resources={r"/*": {"origins": allowed_origins_list}})

if __name__ == "__main__":
    app.run(debug=True)
