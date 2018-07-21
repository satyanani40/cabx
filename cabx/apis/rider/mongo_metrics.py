import sys
import uuid
import linecache
import traceback
import json
from flask import request
from datetime import datetime
from flask_restplus import Namespace, Resource, fields

from feqor.app import logger
from feqor.utils import constants
from feqor.utils import helpers
from feqor.utils import http
from feqor.db.mongodb import DB


mongodb_metrics_ns = Namespace(
    'mongodb-metrics',
    description='Read and Write operations for MongoDB Data Metrics'
)

feqor_metrics_mdl = mongodb_metrics_ns.model('feqor_metrics', {
    'CHIP_NAME_REV': fields.String(required=True, description='combination of chip_name and revision, ex: hana_1.0'),
    'IP_NAME': fields.String(required=True),
    'IP_TYPE': fields.String(required=True),
    'MTIME': fields.Integer(required=True),
    'DATA_TYPE': fields.String(required=True),
})

@mongodb_metrics_ns.route('/feqor-metrics')
class FeqorMetrics(Resource):
    """
    Fetch and Create feqor-metric records
    """
    def get(self):
        '''List FEQoR Metrics'''
        try:
            self_logger = logger.bind(request_id=str(uuid.uuid4()), request_url=request.url)
            query = json.loads(request.args.get('query', '{}'))
            sort = json.loads(request.args.get('sort', '{}'))
            projection = json.loads(request.args.get('projection', '{}'))
            skip = int(request.args.get('skip', 0))
            limit = int(request.args.get('limit', constants.MAX_PAGE_SIZE))
            db_con_obj = DB(self_logger)
            data = db_con_obj.fetch(
                constants.FEQOR_METRICS,query,
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
            created_doc = db_con_obj.create(constants.FEQOR_METRICS, payload)
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


@mongodb_metrics_ns.route('/handoff')
class HandOffMetrics(Resource):
    """
    Fetch and Create feqor-metric records
    """
    def get(self):
        '''List FEQoR Metrics'''
        try:
            self_logger = logger.bind(request_id=str(uuid.uuid4()), request_url=request.url)
            query = json.loads(request.args.get('query', '{}'))
            sort = json.loads(request.args.get('sort', '{}'))
            projection = json.loads(request.args.get('projection', '{}'))
            skip = int(request.args.get('skip', 0))
            limit = int(request.args.get('limit', constants.MAX_PAGE_SIZE))
            db_con_obj = DB(self_logger)
            data = db_con_obj.fetch(
                constants.HANDOFF,query,
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

    @helpers.ensure_post_data
    def post(self, *args, **kwargs):
        try:
            self_logger = logger.bind(request_id=str(uuid.uuid4()), request_url=request.url)
            payload = self.api.payload
            db_con_obj = DB(self_logger)
            self_logger = db_con_obj.logger
            created_doc = db_con_obj.create(constants.HANDOFF, payload)
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

@mongodb_metrics_ns.route('/handoff-waiver')
class HandOffWaiverMetrics(Resource):
    """
    Fetch and Create feqor-metric records
    """
    def get(self):
        '''List FEQoR Metrics'''
        try:
            self_logger = logger.bind(request_id=str(uuid.uuid4()), request_url=request.url)
            query = json.loads(request.args.get('query', '{}'))
            sort = json.loads(request.args.get('sort', '{}'))
            projection = json.loads(request.args.get('projection', '{}'))
            skip = int(request.args.get('skip', 0))
            limit = int(request.args.get('limit', constants.MAX_PAGE_SIZE))
            db_con_obj = DB(self_logger)
            data = db_con_obj.fetch(
                constants.HANDOFF_WAIVER,query,
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

    @helpers.ensure_post_data
    def post(self, *args, **kwargs):
        try:
            self_logger = logger.bind(request_id=str(uuid.uuid4()), request_url=request.url)
            payload = self.api.payload
            db_con_obj = DB(self_logger)
            self_logger = db_con_obj.logger
            created_doc = db_con_obj.create(constants.HANDOFF_WAIVER, payload)
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

@mongodb_metrics_ns.route('/hm-info')
class HMInfo(Resource):
    """
    Fetch and Create feqor-metric records
    """
    def get(self):
        '''List FEQoR Metrics'''
        try:
            self_logger = logger.bind(request_id=str(uuid.uuid4()), request_url=request.url)
            query = json.loads(request.args.get('query', '{}'))
            sort = json.loads(request.args.get('sort', '{}'))
            projection = json.loads(request.args.get('projection', '{}'))
            skip = int(request.args.get('skip', 0))
            limit = int(request.args.get('limit', constants.MAX_PAGE_SIZE))
            db_con_obj = DB(self_logger)
            data = db_con_obj.fetch(
                constants.HM_INFO,query,
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

    @helpers.ensure_post_data
    def post(self, *args, **kwargs):
        try:
            self_logger = logger.bind(request_id=str(uuid.uuid4()), request_url=request.url)
            payload = self.api.payload
            db_con_obj = DB(self_logger)
            self_logger = db_con_obj.logger
            created_doc = db_con_obj.create(constants.HM_INFO, payload)
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



@mongodb_metrics_ns.route('/mem-min-period')
class MemMinPerioid(Resource):
    """
    Fetch and Create feqor-metric records
    """
    def get(self):
        '''List FEQoR Metrics'''
        try:
            self_logger = logger.bind(request_id=str(uuid.uuid4()), request_url=request.url)
            query = json.loads(request.args.get('query', '{}'))
            sort = json.loads(request.args.get('sort', '{}'))
            projection = json.loads(request.args.get('projection', '{}'))
            skip = int(request.args.get('skip', 0))
            limit = int(request.args.get('limit', constants.MAX_PAGE_SIZE))
            db_con_obj = DB(self_logger)
            data = db_con_obj.fetch(
                constants.MEM_MIN_PERIOD,query,
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

    @helpers.ensure_post_data
    def post(self, *args, **kwargs):
        try:
            self_logger = logger.bind(request_id=str(uuid.uuid4()), request_url=request.url)
            payload = self.api.payload
            db_con_obj = DB(self_logger)
            self_logger = db_con_obj.logger
            created_doc = db_con_obj.create(constants.MEM_MIN_PERIOD, payload)
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

