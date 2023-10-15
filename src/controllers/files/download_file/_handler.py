import json
from flask import request
from src.config.soap_client import soap_client


def download_file_handler(token, file_uuid):
    try:
        request_data = {"fileUUID": file_uuid, "token": token}
        response = soap_client.service.file_download(request_data)

        if response["error"] is True:
            return {"msg": response["msg"]}, response["code"]
        else:
            return {"msg": "File downloaded successfully"}, 200

    except ValueError:
        return {"msg": "Invalid JSON data provided in the request"}, 400

    except Exception:
        return {"msg": "There was an error downloading the file"}, 500
