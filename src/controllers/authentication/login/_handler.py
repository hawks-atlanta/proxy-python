import json
from flask import request
from src.config.soap_client import soap_client


def login_handler():
    try:
        data = json.loads(request.data)
        username = data.get("username")
        password = data.get("password")

        not_valid_username = not username or len(username) == 0
        not_valid_password = not password or len(password) == 0
        if not_valid_username or not_valid_password:
            return {"msg": "Required fields are missing in JSON data"}, 400

        result = soap_client.service.auth_login(
            {"username": username, "password": password}
        )

        if result.auth is not None:
            jwt = result.auth.token
            return {"msg": "Login successful", "token": jwt}, 200

        return {"msg": "Invalid credentials"}, 401

    except ValueError:
        return {"msg": "Invalid JSON data provided in the request"}, 400

    except Exception as e:
        print("[Exception] login_handler ->", e)
        return {"msg": "There was an error logging in"}, 500
