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
            return {"msg": "Register succeeded", "jwt": jwt}, 200

        return {"msg": "Username already registered"}, 409

    except Exception as e:
        print("SOAP Error:", str(e))
        return {"msg": "Internal error", "error": str(e)}, 500
