import json
from flask import request
from src.config.soap_client import soap_client
from src.lib.helpers import is_valid_uuid


def file_move_handler(token, file_uuid):
    try:
        data = json.loads(request.data)
        target_directory_uuid = data.get("targetDirectoryUUID")

        not_valid_target_directory = not target_directory_uuid or not is_valid_uuid(
            target_directory_uuid
        )
        if not_valid_target_directory:
            return {"msg": "The target directory is not valid or was not provided"}, 400

        request_data = {
            "token": token,
            "fileUUID": file_uuid,
            "targetDirectoryUUID": target_directory_uuid,
        }

        response = soap_client.service.file_move(request_data)

        if response["error"] is True:
            return {"msg": response["msg"]}, response["code"]
        else:
            return {"msg": "The file has been moved"}, 200

    except ValueError:
        return {"msg": "Not valid JSON data provided in the request"}, 400

    except Exception as e:
        print("[Exception] file_move_handler ->", e)
        return {"msg": "There was an error moving the file"}, 500
