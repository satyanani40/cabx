import json
import os
from datetime import datetime
from bson import ObjectId
from structlog import get_logger

from cabx.utils import constants

logger = get_logger()
ENVIRONMENT = os.getenv("ENVIRONMENT", constants.LOCAL)

logger.info("environment is set.", environment=ENVIRONMENT)
DEBUG = ENVIRONMENT == "local"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# finding configuration file
config_file_path = os.path.join(BASE_DIR, 'configurations', ENVIRONMENT+'_conf.json')


if not os.path.exists(config_file_path):
    exit(constants.CONFIGURATION_FILE_NOT_FOUND.format(config_file_path))

# reading configuration file
with open(config_file_path) as _file:
    data = json.load(_file)

APP_PORT = data.get("app_port", constants.APP_PORT)

os.environ["APP_PORT"] = str(APP_PORT)

logger = logger.bind(ENVIRONMENT=ENVIRONMENT, config_file_path=config_file_path, APP_PORT=APP_PORT)

# mongo connection details
MONGO_URI = data['mongo_uri']
MONGO_DBNAME = data['mongo_dbname']

logger.info("mongodb database found.", db_name=MONGO_DBNAME)

# Custom Encoder
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


RESTPLUS_JSON = {'separators': (', ', ': '),
                'indent': 2,
                'cls': JSONEncoder}

# to validate restplus model
RESTPLUS_VALIDATE = True
logger.info("configuration reading done.")