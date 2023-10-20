from src.config.soap_client import soap_client


def remove_file_handler(token, file_uuid):
    try:
        request_data = {"fileUUID": file_uuid, "token": token}
        response = soap_client.service.file_delete(request_data)

        if response["error"] is True:
            return {"msg": response["msg"]}, response["code"]
        else:
            return {"msg": "File successfully deleted"}, 200

    except Exception as e:
        print("[Exception] remove_file_handler ->", e)
        return {"msg": "There was an error deleting the file"}, 500
