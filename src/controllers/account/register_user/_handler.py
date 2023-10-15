import json
from flask import request
from src.config.soap_client import soap_client


def register_handler():
    try:
        # Get JSON data from the request
        data = json.loads(request.data)
        username = data.get("username")
        password = data.get("password")

        not_valid_username = not username or len(username) == 0
        not_valid_password = not password or len(password) == 0
        if not_valid_username or not_valid_password:
            return {"msg": "Required fields are missing in JSON data"}, 400

        result = soap_client.service.account_register(
            {"username": username, "password": password}
        )

        if result.auth is not None:
            jwt = result.auth.token
            return {"msg": "Register succeeded", "token": jwt}, 200

        return {"msg": "Username already registered"}, 409

    except ValueError:
        return {"msg": "Invalid JSON data provided in the request"}, 400

    except Exception as e:
        print("[Exception] register_handler ->", e)
        return {"msg": "There was an error registering the user"}, 500
