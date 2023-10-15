from src.config.soap_client import soap_client
from src.lib.helpers import is_valid_uuid


def check_state_handler(token, file_uuid):
    try:
        not_valid_file_uuid = not file_uuid or not is_valid_uuid(file_uuid)
        if not_valid_file_uuid:
            return {"msg": "Not valid file UUID provided"}, 400

        response = soap_client.service.file_check(
            {"token": token, "fileUUID": file_uuid}
        )

        has_success_code = str(response.code).startswith("20")
        if not has_success_code:
            return {"msg": response.msg}, response.code

        return {
            "msg": "File status has been obtained successfully",
            "ready": response.ready,
        }, response.code
    except Exception as e:
        print("[Exception] check_state_handler ->", str(e))
        return {"msg": "There was an error checking the file state"}, 500
