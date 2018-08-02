import sys
import uuid
import linecache
import traceback
import json

from flask import request
from flask_restplus import abort
from datetime import timedelta
from flask_restplus import Namespace, Resource, fields


from cabx.app import logger
from cabx.utils import constants
from cabx.utils import helpers
from cabx.utils import http
from cabx.utils import common_utils
from cabx.db.mongodb import DB

user_service_ns = Namespace(
    'user-service',
    description='It will used to create rider details as well as login for both rider and driver'
)

user_model = user_service_ns.model('User', {
    'full_name': fields.String(required=True),
    constants.MOBILE_NUMBER: fields.String(required=True)
})

@user_service_ns.route('/user-login')
class UserLogin(Resource):
    """
    user login authentication
    """

    @user_service_ns.errorhandler
    def get(self):
        '''List Users'''
        request_id =  common_utils.get_request_id()
        return_message = {constants.REQUEST_ID:request_id}
        try:

            self_logger = logger.bind(request_id=request_id, request_url=request.url)
            mobile_number = request.args.get(constants.MOBILE_NUMBER, None)
            otp = request.args.get(constants.OTP, None)
            self_logger.info("given login parameters", mobile_number=mobile_number, otp=otp)
            if not mobile_number:
                message = "mobile number should not be empty"
                self_logger.error(message)
                return_message.update(message=message)
                return return_message, 400
            if not otp:
                message = "otp should not be empty"
                self_logger.error(message)
                return_message.update(message=message)
                return return_message, 400

            query = {constants.MOBILE_NUMBER: mobile_number, constants.OTP:otp}
            projection = json.loads(request.args.get('projection', '{}'))
            db_con_obj = DB(self_logger)
            data = db_con_obj.fetch_one(constants.USERS,query,projection=projection)
            self_logger = db_con_obj.logger
            if data:
                # create access_token and activate user
                access_token_creation_payload = {
                    constants.MOBILE_NUMBER: data[constants.MOBILE_NUMBER],
                    constants.OTP: data[constants.OTP]
                }
                payload = {
                    constants.OTP: "",
                    constants.IS_ACTIVE: True,
                    constants.ACCESS_TOKEN: common_utils.create_access_token(access_token_creation_payload)
                }
                return db_con_obj.find_one_update_or_create(constants.USERS, query, payload)
            else:
                message = "Invalid OTP"
                self_logger.info(message)
                return_message.update(message=message)
                return return_message,400
        except Exception as e:
            #exc_type, exc_value, exc_traceback = sys.exc_info()
            #message = repr(traceback.format_exception(exc_type, exc_value,
            #                                          exc_traceback))
            self_logger.error(str(e))
            error_code = getattr(e, 'code', http.UNPROCESSABLE_REQUEST.code)
            if error_code not in constants.POSSIBLE_EXCEPTIONS:
                error_code = http.UNPROCESSABLE_REQUEST.code
            return_message.update(message=str(e))
            return return_message, error_code


@user_service_ns.route('/user-registration')
class RiderRegistration(Resource):
    """
    It will creates user
    """
    @user_service_ns.errorhandler
    @user_service_ns.expect(user_model)
    @user_service_ns.marshal_with(user_model, envelope='data')
    def post(self, *args, **kwargs):
        request_id = str(uuid.uuid4())
        return_message = {constants.REQUEST_ID:request_id}
        try:
            '''Create User: full name,OTP and send OTP to registered mobile '''
            self_logger = logger.bind(request_id=request_id, request_url=request.url)
            payload = self.api.payload
            db_con_obj = DB(self_logger)
            self_logger = db_con_obj.logger
            payload[constants.IS_ACTIVE] = False
            payload[constants.ACCESS_TOKEN] = ""
            ## get user OTP if it is already exists else generate OTP
            # generate registration OTP or token
            query = {constants.MOBILE_NUMBER: payload[constants.MOBILE_NUMBER]}
            projection = {constants.OTP:1, constants.OTP_EXPIRE_DATE:1, constants.MOBILE_NUMBER:1}
            data = db_con_obj.fetch_one(constants.USERS, query, projection=projection)
            if data is not None:
                self_logger.info("user already registerd", mobile_number = payload[constants.MOBILE_NUMBER])
                # if record already created with above mobile number, do following things.
                # 1. check OTP expire date, if not expire take same otp, change user active to not active
                present_date_time = common_utils.get_current_datetime()
                expire_date = data[constants.OTP_EXPIRE_DATE]
                self_logger.info("present_time:{}, expire_date:{}".format(present_date_time, expire_date))
                # checking expired or not, if false expired, if true  not expired.
                if present_date_time > expire_date:
                    generated_token = common_utils.generate_otp()
                    self_logger.info("token expired", generated_token=generated_token)
                    payload[constants.OTP] = generated_token
                else:
                    self_logger.info("token not expired", OTP=data[constants.OTP])
                    payload[constants.OTP] = data[constants.OTP]

            else:
                self_logger.info("user not registered previously", mobile_number=payload[constants.MOBILE_NUMBER])
                payload[constants.OTP] = common_utils.generate_otp()
                payload[constants.OTP_EXPIRE_DATE] = common_utils.get_current_datetime() + timedelta(minutes =constants.OTP_EXPIRE_MINUTES)\

            payload[constants.USER_TYPE] = constants.DEFAULT_USER
            # send otp to mobile
            is_sms_send = common_utils.send_mobile_message(payload[constants.MOBILE_NUMBER])
            if is_sms_send:
                self_logger.info("sms send successfully.", mobile_number = payload[constants.MOBILE_NUMBER])
                query = {constants.MOBILE_NUMBER: payload[constants.MOBILE_NUMBER]}
                created_doc = db_con_obj.find_one_update_or_create(constants.USERS,query, payload, True)
                self_logger.info("created document id {}".format(created_doc['_id']))
                return created_doc, http.SUCCESS.code
            message = "faild to send sms to:{mobile_number}".format(mobile_number = payload[constants.MOBILE_NUMBER])
            self_logger.error(message)
            return_message.update(message=message)
            return return_message, http.UNPROCESSABLE_REQUEST.code
        except Exception as e:
            error_code = getattr(e,'code',http.UNPROCESSABLE_REQUEST.code)
            if error_code not in constants.POSSIBLE_EXCEPTIONS:
                error_code = http.UNPROCESSABLE_REQUEST.code
            return_message.update(message=str(e))
            return return_message, error_code


