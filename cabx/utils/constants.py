APPLICATION_NAME = "CABX API"
VERSION = "1.0.0"
DESCRIPTION = "Cab Services for Riders and Drivers."
LOGGING_TS_FORMAT = "%Y-%m-%d %H:%M:%S"
MONGO_DOC_CREATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
LOCAL="local"
CONFIGURATION_FILE_NOT_FOUND = "configuration file path:{} not found"
APP_PORT = 8000
MAX_PAGE_SIZE = 2000
OTP_EXPIRE_MINUTES = 1

API_SECRET = "314b1##@@$$e8@@717$$174c177c5570b246X4958!!1dea2111d&&105Aa623df82e1c97a302f8!!9832593eff331ff"

# other constants
REQUEST_ID="request_id"
REQUEST_METHOD="method"
REQUEST_URL="url"
EVENT = "event"
TIMESTAMP="timestamp"
CREATED_DATE = "t_created_date"

# EXCEPTION CONSTANTS
POSSIBLE_EXCEPTIONS = [400,401,403,404,500,422]


# MONGODB  COLLECTION NAMES
USERS = "users"
# mognodb reference field names format should be like
#DB_REFS = {"collection_name":[]}
DB_REFS = {
}

# mongodb collection field constants
IS_ACTIVE = "is_active"
MOBILE_NUMBER = "mobile_number"
OTP = "otp"
OTP_EXPIRE_DATE = "otp_expire_date"
ACCESS_TOKEN = "access_token"
CURRENT_DATE_TIME = "current_date_time"

MIN_RANDOM_NUM = 100000
MAX_RANDOM_NUM = 999999
USER_TYPE = "user_type"
RIDER = "rider"
DRIVER = "driver"
DEFAULT_USER = RIDER