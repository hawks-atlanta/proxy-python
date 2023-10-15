import json
from flask import request
from src.config.soap_client import soap_client
from src.lib.helpers import is_valid_uuid


def rename_handler(token, file_uuid):
    try:
        data = json.loads(request.data)

        # Validate new name
        new_name = data["newName"]
        if not new_name or len(new_name) == 0:
            return {"msg": "New name is required"}, 400

        # Validate file UUID
        not_valid_file_uuid = not file_uuid or not is_valid_uuid(file_uuid)
        if not_valid_file_uuid:
            return {"msg": "Not valid file UUID provided"}, 400

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
