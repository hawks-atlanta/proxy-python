from flask import request
from src.config.soap_client import soap_client


def login_handler():
    try:
        # Get JSON data from the request
        data = request.json

        if not data:
            return {"msg": "No JSON data provided in the request"}, 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"msg": "Required fields are missing in JSON data"}, 400

        result = soap_client.service.auth_login(
            {"username": username, "password": password}
        )

        if result.auth is not None:
            jwt = result.auth.token
            return {"msg": "Login successful", "jwt": jwt}, 200

        return {"msg": "Invalid credentials"}, 401

    except Exception as e:
        print("SOAP Error:", str(e))
        return {"msg": "Internal error", "error": str(e)}, 500


def challenge():
    try:
        data = request.json

        if not data:
            return {"msg": "No JSON data provided in the request"}, 400

        token = data.get("jwt")

        if not token:
            return {"msg": "Token is missing in JSON data"}, 400

        response = soap_client.service.auth_refresh({"token": token})

        print(response)

        if hasattr(response, "auth") and hasattr(response.auth, "token"):
            jwt = response.auth.token
            return {
                "msg": "JWT refreshed successfully",
                "jwt": jwt,
            }, 200
        else:
            return {"msg": response.msg}, response.code

    except Exception as e:
        print("Error:", str(e))
        return {"msg": "Internal error: " + str(e)}, 500
