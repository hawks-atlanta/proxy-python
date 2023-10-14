from flask import request
from werkzeug.utils import secure_filename
from src.config.soap_client import soap_client
from src.lib.helpers import is_valid_uuid


def upload_file_handler(token):
    try:
        if "file" not in request.files or "location" not in request.form:
            return {"msg": "Required fields are missing in form data"}, 400

        # Get file from request
        file = request.files["file"]

        # Set null if file location is am empty string
        fileLocation = request.form["location"]
        fileLocation = None if fileLocation == "" else fileLocation

        # Check if fileLocation is a valid UUID
        not_valid_location = fileLocation is not None and not is_valid_uuid(
            fileLocation
        )
        if not_valid_location:
            return {"msg": "Not valid file location provided"}, 400

        # Separate file name from extension
        fileName = secure_filename(file.filename)
        result = soap_client.service.file_upload(
            {
                "fileName": fileName,
                "fileContent": file.read(),
                "location": fileLocation,
                "token": token,
            }
        )

        if result.fileUUID is None:
            return {"msg": result["msg"]}, result["code"]

        fileId = result.fileUUID
        return {"msg": "The file is being uploaded", "fileUUID": fileId}, 201

    except Exception as e:
        print("[Exception] file_download_handler ->", str(e))
        return {"msg": "Internal error", "error": str(e)}, 500
