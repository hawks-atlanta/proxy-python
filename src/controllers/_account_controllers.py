import json
from flask import request
from src.config.soap_client import soap_client


def register_handler():
    try:
        # Get JSON data from the request
        data = request.json

        if not data:
            return {"msg": "No JSON data provided in the request"}, 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"msg": "Required fields are missing in JSON data"}, 400

        result = soap_client.service.account_register(
            {"username": username, "password": password}
        )

        if result.auth is not None:
            jwt = result.auth.token
            return {"msg": "Register succeeded", "token": jwt}, 200

        return {"msg": "Username already registered"}, 409

    except Exception as e:
        print("[Exception] register_handler ->", str(e))
        return {"msg": "There was an error registering the user"}, 500


def update_password_handler(token):
    try:
        data = json.loads(request.data)
        oldPassword = data.get("oldPassword")
        newPassword = data.get("newPassword")

        if not oldPassword or not newPassword or not token:
            return {"msg": "Required fields are missing in JSON data"}, 400

        result = soap_client.service.account_password(
            {"oldpassword": oldPassword, "newpassword": newPassword, "token": token}
        )

        if result["error"] is True:
            return {"msg": result["msg"]}, result["code"]
        else:
            return {"msg": "Password updated successfully"}, 200

    except ValueError:
        return {"msg": "Invalid JSON data provided in the request"}, 400

    except Exception as e:
        print("[Exception] password_handler ->", str(e))
        return {"msg": "Internal error", "error": str(e)}, 500
