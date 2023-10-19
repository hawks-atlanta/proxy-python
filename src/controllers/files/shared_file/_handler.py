from src.config.soap_client import soap_client


def shared_files_handler(token):
    try:
        request_data = {"token": token}
        response = soap_client.service.share_list(request_data)

        if response["error"] is True:
            return {"msg": response["msg"]}, response["code"]

        files = [
            {
                "name": file.name,
                "size": file.size,
                "isFile": file.isFile,
                "extension": file.extension,
                "uuid": file.uuid,
                "ownerusername": file.ownerusername,
            }
            for file in response.files
        ]

        return {
            "files": files,
            "msg": "List of shared files obtained",
        }, 200
    except Exception as e:
        print("[Exception] shared_files_handler ->", e)
        return {"msg": "There was an error listing the shared files"}, 500