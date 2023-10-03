import flask
from flask import request
from zeep import Client


view = flask.Blueprint("home", __name__)

# connect
client = Client("http://localhost:8080/service?wsdl")


@view.route("/", methods=["GET"])
def index():
    return flask.render_template("index.html")


@view.route("/auth_login", methods=["POST"])
def auth_login():
    try:
        # Get JSON data from the request
        data = request.json

        if not data:
            return {"message": "No JSON data provided in the request"}, 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"message": "Required fields are missing in JSON data"}, 400

        result = client.service.auth_login({"username": username, "password": password})

        print(result)

        if result.auth is not None:
            token = result.auth.token
            return {"message": "Login successful", "token": token}, 200
        else:
            return {"message": "Invalid credentials"}, 401

    except Exception as e:
        print("SOAP Error:", str(e))
        return {"message": "Internal error", "error": str(e)}, 500
