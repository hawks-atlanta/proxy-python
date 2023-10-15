from src.config.soap_client import soap_client


def challenge_handler(token):
    try:
        response = soap_client.service.auth_refresh({"token": token})
        if hasattr(response.auth, "token"):
            refreshed_token = response.auth.token
            return {
                "msg": "JWT refreshed successfully",
                "token": refreshed_token,
            }, 200
        else:
            return {"msg": response.msg}, response.code

    except Exception as e:
        print("[Exception] challenge ->", e)
        return {"msg": "There was an error validating or refreshing the session"}, 500
