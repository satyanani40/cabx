import sys
import uuid
import linecache
import traceback
import json
from flask import request
from datetime import datetime
from flask_restplus import Namespace, Resource, fields

from cabx.app import logger
from cabx.utils import constants
from cabx.utils import helpers
from cabx.utils import http
from cabx.db.mongodb import DB


authentication_ns = Namespace(
    'authentication',
    description='User create and login services'
)

user_model = authentication_ns.model('authentication', {
    'full_name': fields.String(required=True, description='combination of chip_name and revision, ex: hana_1.0'),
    'mobile_number': fields.String(required=True),
    'is_active': fields.Boolean(default=False),
    'login_token': fields.String(),
    'registration_token': fields.String()
})

@mongodb_metrics_ns.route('/create-user')
class FeqorMetrics(Resource):
    """
    Fetch and Create user(s)
    """
    def get(self):
        '''List Users'''
        try:
            self_logger = logger.bind(request_id=str(uuid.uuid4()), request_url=request.url)
            query = json.loads(request.args.get('query', '{}'))
            sort = json.loads(request.args.get('sort', '{}'))
            projection = json.loads(request.args.get('projection', '{}'))
            skip = int(request.args.get('skip', 0))
            limit = int(request.args.get('limit', constants.MAX_PAGE_SIZE))
            db_con_obj = DB(self_logger)
            data = db_con_obj.fetch(
                constants.USERS,query,
                sort=sort, projection=projection, skip=skip, limit=limit
            )
            self_logger = db_con_obj.logger
            return {
                "status": http.SUCCESS.status,
                "data": data
            }
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            message = repr(traceback.format_exception(exc_type, exc_value,
                                                      exc_traceback))
            self_logger.error(message)
            result = {"status": http.BAD_REQUEST.status, "message": str(e)}
            return result, http.BAD_REQUEST.code

    #@helpers.ensure_post_data
    @mongodb_metrics_ns.expect(feqor_metrics_mdl)
    def post(self, *args, **kwargs):
        try:
            self_logger = logger.bind(request_id=str(uuid.uuid4()), request_url=request.url)
            payload = self.api.payload
            db_con_obj = DB(self_logger)
            self_logger = db_con_obj.logger
            created_doc = db_con_obj.create(constants.USERS, payload)
            self_logger.info("created document id {}".format(created_doc['_id']))
            return {
                "status": http.SUCCESS.status,
                "data": created_doc
            }
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            message = repr(traceback.format_exception(exc_type, exc_value,
                                                      exc_traceback))
            self_logger.error(message)
            result = {"status": http.BAD_REQUEST.status, "message": str(e)}
            return result, http.BAD_REQUEST.code