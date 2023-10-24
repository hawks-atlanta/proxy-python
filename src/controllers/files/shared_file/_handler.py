from src.config.soap_client import soap_client


def shared_files_handler(token):
    try:
        request_data = {"token": token}
        response = soap_client.service.share_list(request_data)

        if response["error"] is True:
            return {"msg": response["msg"]}, response["code"]

        files = [
            {
                "extension": file.extension,
                "name": file.name,
                "isFile": file.isFile,
                "uuid": file.uuid,
                "size": file.size,
            }
            for file in response.sharedFiles
        ]

        return {
            "files": files,
            "msg": "List of shared files obtained",
        }, 200
    except Exception as e:
        print("[Exception] shared_files_handler ->", e)
        return {"msg": "There was an error listing the shared files"}, 500
