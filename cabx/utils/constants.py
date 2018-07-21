APPLICATION_NAME = "FEQoR API"
VERSION = "1.0.0"
DESCRIPTION = "Data Operation On FEQoR Mongo Data & File System."
LOGGING_TS_FORMAT = "%Y-%m-%d %H:%M:%S"
MONGO_DOC_CREATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
LOCAL="local"
CONFIGURATION_FILE_NOT_FOUND = "configuration file path:{} not found"
APP_PORT = 8000
MAX_PAGE_SIZE = 2000

# other constants
REQUEST_ID="request_id"
REQUEST_METHOD="method"
REQUEST_URL="url"
EVENT = "event"
TIMESTAMP="timestamp"
CREATED_DATE = "t_created_date"

# MONGODB  COLLECTION NAMES
USERS = "users"
# mognodb reference field names format should be like
#DB_REFS = {"collection_name":[]}
DB_REFS = {
}