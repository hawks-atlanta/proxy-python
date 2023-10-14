import json
from flask import request
from src.config.soap_client import soap_client


def create_new_dir_handler(token):
    try:
        data = json.loads(request.data)

        directoryName = data.get("directoryName")
        location = data.get("location")

        if not directoryName or not location:
            return {"msg": "Required fields are missing in JSON data"}, 400

        response = soap_client.service.file_new_dir(
            {
                "directoryName": directoryName,
                "location": location,
                "token": token,
            }
        )

        if response["error"] is True:
            return {"msg": response["msg"]}, response["code"]
        else:
            return {
                "msg": "New directory created successfully",
                "directoryUUID": response["fileUUID"],
            }, response["code"]

    except ValueError:
        return {"msg": "Invalid JSON data provided in the request"}, 400

    except Exception as e:
        print("[Exception] create_new_directory ->", str(e))
        return {"msg": "There was an error creating the new directory"}, 500
