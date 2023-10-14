import json
from flask import request
from src.config.soap_client import soap_client


def rename_handler(token, file_uuid):
    try:
        data = json.loads(request.data)
        new_name = data["newName"]
        if not new_name or len(new_name) == 0:
            return {"msg": "New name is required"}, 400

        request_data = {"token": token, "fileUUID": file_uuid, "newName": new_name}
        response = soap_client.service.file_rename(request_data)

        if response["error"] is True:
            return {"msg": response["msg"]}, response["code"]
        else:
            return {"msg": "The file has been renamed successfully"}, 200

    except ValueError:
        return {"msg": "Invalid JSON data provided in the request"}, 400

    except Exception:
        return {"msg": "There was an error renaming the file"}, 500
