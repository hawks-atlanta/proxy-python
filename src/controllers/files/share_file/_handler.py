import json
from flask import request
from src.config.soap_client import soap_client


def share_handler(token):
    try:
        data = json.loads(request.data)

        fileUUID = data["fileUUID"]
        otherUsername = data["otherUsername"]

        if not fileUUID or not otherUsername or not token:
            return {"msg": "Required fields are missing in form data"}, 400

        request_data = {
            "fileUUID": fileUUID,
            "otherUsername": otherUsername,
            "token": token,
        }
        response = soap_client.service.share_file(request_data)

        if response["error"] is True:
            return {"msg": response["msg"]}, response["code"]
        else:
            return {"msg": "File shared successfully"}, 200

    except ValueError:
        return {"msg": "Invalid JSON data provided in the request"}, 400

    except Exception:
        return {"msg": "There was an error sharing the file"}, 500
