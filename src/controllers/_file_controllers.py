from src.config.soap_client import soap_client


def check_state_handler(token, file_uuid):
    try:
        response = soap_client.service.file_check(
            {"token": token, "fileUUID": file_uuid}
        )

        has_success_code = str(response.code).startswith("20")
        if not has_success_code:
            return {"msg": response.msg}, response.code

        return {"msg": response.msg, "ready": response.ready}, response.code
    except Exception as e:
        print("[Exception] check_state_handler ->", str(e))
        return {"msg": "There was an error checking the file state"}, 500
