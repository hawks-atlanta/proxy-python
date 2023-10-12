from flask import request
from src.config.soap_client import soap_client


def upload_file_handler():
    try:
        # Get JSON data from the request
        data = request.json

        if not data:
            return {"msg": "No JSON data provided in the request"}, 400

        file = data.get("file")
        fileName = data.get("fileName")
        location = data.get("location")

        if not fileName or not location or not file:
            return {"msg": "Failed field validation."}, 400

        result = soap_client.service.file_upload(
            {"file": file, "location": location, "fileName": fileName}
        )

        if result.fileUUID is not None:
            fileId = result.fileUUID
            return {"msg": "File upload successful.", "fileUUID": fileId}, 201

        return {"msg": "Bad request. File is too large."}, 413

    except Exception as e:
        print("[Exception] register_handler ->", str(e))
        return {"msg": "Internal error", "error": str(e)}, 500
