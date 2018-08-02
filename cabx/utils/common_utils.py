import uuid
import jwt
from datetime import datetime, timezone
from random import randint


from cabx.utils import constants

def send_mobile_message(phone_number, **kwargs):
    """
    Not yet implemented.
    :param phone_number:
    :param kwargs:
    :return:
    """
    # TODO: not yet implemented. once we got message service details will finish it.
    return True

def generate_otp():
    return randint(constants.MIN_RANDOM_NUM, constants.MAX_RANDOM_NUM)

def get_current_datetime(timezone=timezone.utc):
    return datetime.now(timezone)

def create_access_token(payload):
    payload.update({constants.CURRENT_DATE_TIME: get_current_datetime()})
    return jwt.encode(payload, constants.API_SECRET, algorithm='HS256')

def decode_access_token(encoded_token):
    return jwt.decode(encoded_token, constants.API_SECRET, algorithms=['HS256'])

def format_error_exception(error):
    if error_code in [11000]:
        field = error.message.split(".$")[1]
        field = field.split(" dup key")[0]
        field = field.substring(0, field.lastIndexOf("_"))
        return 11000, field
    return 422, ""

def get_request_id():
    return str(uuid.uuid4())
