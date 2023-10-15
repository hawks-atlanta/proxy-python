import flask
from src.config.soap_client import soap_client
from src.lib.helpers import is_valid_uuid


def list_files_handler(token):
    try:
        directory_uuid = flask.request.args.get("directoryUUID", None)

        # Validate directoryUUID
        not_valid_directory_uuid = directory_uuid is not None and not is_valid_uuid(
            directory_uuid
        )

        if not_valid_directory_uuid:
            return {"msg": "Not valid directory UUID provided"}, 400

        # Send the request
        request_data = {"token": token, "location": directory_uuid}
        response = soap_client.service.file_list(request_data)

        if response.error is True:
            return {"error": response.msg}, response.code

        # Parse files into dict
        files = [
            {
                "name": file.name,
                "extension": file.extension,
                "isFile": file.isFile,
                "uuid": file.uuid,
                "size": file.size,
            }
            for file in response.files
        ]

        return {
            "files": files,
            "msg": "Files have been listed successfully",
        }, 200
    except Exception as e:
        print("[Exception] list_files_handler ->", e)
        return {"msg": "There was an error listing the files"}, 500
