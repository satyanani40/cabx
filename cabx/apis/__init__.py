from flask import Blueprint
from flask_restplus import Api

from cabx.utils import constants
from cabx.utils import http
from cabx.utils import common_utils

blueprint = Blueprint('api', __name__,  url_prefix='/api')
api = Api(blueprint,
          version=constants.VERSION,
          title=constants.APPLICATION_NAME,
          description=constants.DESCRIPTION
)

@api.errorhandler
def default_error_handler(error):
    '''Default error handler'''
    return {'message': str(error), 'datetime':common_utils.get_current_datetime()}, getattr(error, 'code', http.UNPROCESSABLE_REQUEST.code)

from .user.user_services import user_service_ns
api.add_namespace(user_service_ns)