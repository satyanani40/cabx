from functools import wraps
from flask import request


JSON_HEADER = "application/json"
BAD_CONTENT_TYPE = "Content-Type header must be set to `application/json`"
EMPTY_MSG = "JSON must be non-empty object"
MISSING_KEYS_MSG = "JSON's header property must include these keys: {}"

#
# Helpers for API Handlers
# # # # # # # # # # # # # # # # # # # # # # #
def ensure_post_data(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        if JSON_HEADER not in request.headers.get("Content-Type"):
            result = {"status": "bad_input",
                      "message": BAD_CONTENT_TYPE}
            return result, 400

        data = request.get_json(force=True)
        if not data or not isinstance(data, dict):
            result = {"status": "bad_input",
                      "message": EMPTY_MSG}
            return result, 400
        return fn(*args, data=data, **kwargs)
    return inner

