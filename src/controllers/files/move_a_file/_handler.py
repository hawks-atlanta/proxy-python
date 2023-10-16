from src.config.soap_client import soap_client
from flask import request


def file_move_handler(token, file_uuid):
    try:
        data = request.get_json()
        target_directory_uuid = data.get("targetDirectoryUUID")

        if not target_directory_uuid:
            return {
                "msg": "Required field 'targetDirectoryUUID' is missing in JSON data"
            }, 400

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

    except Exception as e:
        print("[Exception] file_move_handler ->", e)
        return {"msg": "There was an error moving the file"}, 500
