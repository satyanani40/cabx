from functools import wraps
from flask import request

from cabx.utils import constants
from cabx.utils import common_utils


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

def check_access_token(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        if not request.headers.get(constants.ACCESS_TOKEN, None):
            result = {
                "status": "bad_input",
                "message": MISSING_KEYS_MSG.format(constants.ACCESS_TOKEN)
            }
            return result, 400
        access_token = request.headers.get(constants.ACCESS_TOKEN)
        decoded_access_token = common_utils.decode_access_token(access_token)
        if constants._ID not in decoded_access_token:
            result = {
                "status": "invalid token",
                "message": "invalid token:{}".foramt(access_token)
            }
            return result, 401

        kwargs.update({constants.DECODED_TOKEN:decoded_access_token})
        data = request.get_json(force=True)
        return fn(*args, data=data, **kwargs)
    return inner

def check_user_loggedin_or_not(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        if not request.headers.get(constants.ACCESS_TOKEN, None):
            result = {"status": "bad_input",
                      "message": MISSING_KEYS_MSG.format(constants.ACCESS_TOKEN)}
            return result, 400

        data = request.get_json(force=True)
        if not data or not isinstance(data, dict):
            result = {"status": "bad_input",
                      "message": EMPTY_MSG}
            return result, 400
        return fn(*args, data=data, **kwargs)
    return inner
