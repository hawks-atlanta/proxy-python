from src.config.soap_client import soap_client
from src.lib.helpers import is_valid_uuid


def shared_with_who_handler(token, file_uuid):
    try:
        if not is_valid_uuid(file_uuid):
            return {"msg": "Not valid file UUID provided"}, 400

        request_data = {"fileUUID": file_uuid, "token": token}
        response = soap_client.service.share_list_with_who(request_data)

        if response.usernames is None:
            return {"msg": response["msg"]}, response["code"]

        usernames = [
            {
                "users": usernames,
            }
            for usernames in response.usernames
        ]

        return {
            "users": usernames,
            "msg": "List of users the file is shared with",
        }, 200
    except Exception as e:
        print("[Exception] shared_with_who_handler ->", e)
        return {"msg": "There was an error listing the shared with"}, 500