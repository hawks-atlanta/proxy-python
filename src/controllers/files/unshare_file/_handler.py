import json
from flask import request
from src.config.soap_client import soap_client
from src.lib.helpers import is_valid_uuid


def unshare_handler(token):
    try:
        data = json.loads(request.data)
        fileUUID = data["fileUUID"]
        otherUsername = data["otherUsername"]

        # Check if required fields are empty
        empty_file_uuid = not fileUUID or len(fileUUID) == 0
        empty_other_username = not otherUsername or len(otherUsername) == 0
        if empty_file_uuid or empty_other_username:
            return {"msg": "Required fields are missing in form data"}, 400

        # Check if file UUID is valid
        if not is_valid_uuid(fileUUID):
            return {"msg": "Not valid file UUID provided"}, 400

        request_data = {
            "fileUUID": fileUUID,
            "otherUsername": otherUsername,
            "token": token,
        }
        response = soap_client.service.unshare_file(request_data)

        if response["error"] is True:
            return {"msg": response["msg"]}, response["code"]
        else:
            return {"msg": "File unshared successfully"}, 200

    except ValueError:
        return {"msg": "Invalid JSON data provided in the request"}, 400

    except Exception as e:
        print("[Exception] unshare_handler ->", e)
        return {"msg": "There was an error unsharing the file"}, 500
