from src.config.soap_client import soap_client
from src.lib.helpers import is_valid_uuid


def get_file_handler(token, file_uuid):
    try:
        # Check if the file uuid is valid
        not_valid_file_uuid = not file_uuid or not is_valid_uuid(file_uuid)
        if not_valid_file_uuid:
            return {"msg": "Not valid file uuid provided"}, 400

        # Send the request to the SOAP service
        response = soap_client.service.file_get({"token": token, "fileUUID": file_uuid})
        if response.error is True:
            return {"msg": response.msg}, response.code

        response_file = response.file
        return {
            "msg": "The file have been obtained successfully",
            "file": {
                "uuid": response_file.uuid,
                "name": response_file.name,
                "extension": response_file.extension,
                "size": response_file.size,
                "isFile": response_file.isFile,
            },
        }, 200
    except Exception as e:
        print("[Exception] get_file_handler ->", str(e))
        return {"msg": "There was an error while obtaining the file"}, 500
