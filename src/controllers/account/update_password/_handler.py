import json
from flask import request
from src.config.soap_client import soap_client


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
        print("[Exception] password_handler ->", e)
        return {"msg": "Internal error"}, 500
