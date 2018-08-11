import uuid
import jwt
from datetime import datetime, timezone, timedelta
from werkzeug.exceptions import HTTPException
from random import randint


from cabx.utils import constants
from cabx.utils import http

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

def raise_exception(message, message_dict, error_code=http.UNPROCESSABLE_REQUEST.code):
    e = HTTPException(message)
    e.data = message_dict
    e.code = error_code
    raise e

def process_resource_exception_block(logger, e,return_message):
    error_code = getattr(e, 'code', http.INTERNAL_SERVER_ERROR.code)
    if error_code not in constants.POSSIBLE_EXCEPTIONS:
        error_code = http.INTERNAL_SERVER_ERROR.code
    return_message.update(message=str(e))
    logger.error("exception while processing resource", **return_message)
    raise_exception(str(e), return_message, error_code)


def get_current_datetime(timezone=timezone.utc):
    d = datetime.now(timezone)
    return datetime(
        year=d.year, month=d.month, day=d.day, hour=d.hour,
        minute=d.minute, second=d.second, microsecond=d.microsecond
    )

def get_expired_date(expire_time_range=constants.OTP_EXPIRE_TIME_INTERVAL):
    d = get_current_datetime() + timedelta(days=expire_time_range)
    return datetime(
        year=d.year, month=d.month, day=d.day, hour=d.hour,
        minute=d.minute, second=d.second, microsecond=d.microsecond
    )


def create_access_token(payload):
    payload.update({constants.EXP: get_expired_date()})
    return jwt.encode(payload, constants.API_SECRET, algorithm='HS256')

def decode_access_token(encoded_token):
    try:
        return jwt.decode(encoded_token, constants.API_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError as e:
        raise HTTPException("token:{} expired".format(encoded_token), status_code=401)

def format_error_exception(error):
    if error_code in [11000]:
        field = error.message.split(".$")[1]
        field = field.split(" dup key")[0]
        field = field.substring(0, field.lastIndexOf("_"))
        return 11000, field
    return 422, ""

def get_request_id():
    return str(uuid.uuid4())
