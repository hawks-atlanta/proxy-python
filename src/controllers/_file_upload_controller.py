import json
from flask import request
from src.config.soap_client import soap_client


def upload_file_handler(token):
    try:
        data = json.loads(request.data)
        file = data.get("file")
        fileName = data.get("fileName")
        location = data.get("location")

        if not file or not fileName or not location or not token:
            return {"msg": "Required fields are missing in JSON data"}, 400

        result = soap_client.service.file_upload(
            {
                "fileName": fileName,
                "fileContent": file,
                "location": location,
                "token": token,
            }
        )

        if result.fileUUID is None:
            return {"msg": result["msg"]}, result["code"]
        else:
            fileId = result.fileUUID
            return {"msg": "File upload successful.", "fileUUID": fileId}, 201

    except ValueError:
        return {"msg": "Invalid JSON data provided in the request"}, 400

    except Exception as e:
        print("[Exception] file_download_handler ->", str(e))
        return {"msg": "Internal error", "error": str(e)}, 500
