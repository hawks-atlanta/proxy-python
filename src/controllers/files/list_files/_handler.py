import json
import flask
from src.config.soap_client import soap_client


def get_list_handler(token):
    try:
        directory_uuid = flask.request.args.get("directoryUUID", "null")
        request_data = {"token": token, "location": directory_uuid}
        response = soap_client.service.file_list(request_data)

        print(response)

        if hasattr(response, "error") and response.error:
            return json.dumps({"error": response.error})

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

        response_data = {"files": files}
        return json.dumps(response_data)
    except Exception as e:
        return json.dumps({"error": str(e)})
