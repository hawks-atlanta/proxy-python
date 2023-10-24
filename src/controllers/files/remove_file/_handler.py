from src.config.soap_client import soap_client
from src.lib.helpers import is_valid_uuid


def remove_file_handler(token, file_uuid):
    try:
        if not is_valid_uuid(file_uuid):
            return {"msg": "Not valid file UUID provided"}, 400

        request_data = {"fileUUID": file_uuid, "token": token}
        response = soap_client.service.file_delete(request_data)

        if response["error"] is True:
            return {"msg": response["msg"]}, response["code"]
        else:
            return {"msg": "File successfully deleted"}, 200

    except Exception as e:
        print("[Exception] remove_file_handler ->", e)
        return {"msg": "There was an error deleting the file"}, 500
