from flask import request
from src.config.soap_client import soap_client


def login_handler():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return {"msg": "Required fields are missing in JSON data"}, 400

        result = soap_client.service.auth_login(
            {"username": username, "password": password}
        )

        if result.auth is not None:
            jwt = result.auth.token
            return {"msg": "Login successful", "token": jwt}, 200

        return {"msg": "Invalid credentials"}, 401

    except Exception as e:
        print("[Exception] login_handler ->", str(e))
        return {"msg": "Internal error", "error": str(e)}, 500


def challenge_handler(token):
    try:
        response = soap_client.service.auth_refresh({"token": token})
        if hasattr(response.auth, "token"):
            refreshed_token = response.auth.token
            return {
                "msg": "JWT refreshed successfully",
                "token": refreshed_token,
            }, 200
        else:
            return {"msg": response.msg}, response.code

    except Exception as e:
        print("[Exception] challenge ->", str(e))
        return {"msg": "Internal error: " + str(e)}, 500
