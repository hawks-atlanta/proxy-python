from functools import wraps
from flask import request, abort, jsonify, make_response


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Check the token is present as a header
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split("Bearer ")[1]
        if not token:
            abort(make_response(jsonify({"msg": "Token is missing"}), 401))

        # Return the function with the token as a parameter
        return f(token, *args, **kwargs)

    return decorated
