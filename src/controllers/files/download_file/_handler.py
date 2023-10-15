import io
from flask import send_file
from src.config.soap_client import soap_client


def download_file_handler(token, file_uuid):
    try:
        request_data = {"fileUUID": file_uuid, "token": token}
        response = soap_client.service.file_download(request_data)

        if response["error"] is True:
            return {"msg": response["msg"]}, response["code"]
        else:
            response_file = send_file(
                path_or_file=io.BytesIO(response["fileContent"]),
                as_attachment=True,
                mimetype="application/octet-stream",
                download_name=response["fileName"],
            )

            return response_file

    except ValueError:
        return {"msg": "Invalid JSON data provided in the request"}, 400

    except Exception as e:
        print("[Exception] download_file_handler ->", e)
        return {"msg": "There was an error downloading the file"}, 500
