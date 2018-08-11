import sys
import uuid
import linecache
import traceback
import json
import pytz
from flask import request
from flask_restplus import abort
from datetime import timedelta, datetime
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

user_return_fields = user_service_ns.inherit(
    'user_ui_fields', user_model, {
        constants.ACCESS_TOKEN: fields.String,
        constants.USER_TYPE: fields.String
    }
)
@user_service_ns.route('/user-login')
class UserLogin(Resource):
    """
    user login authentication
    """

    @user_service_ns.errorhandler
    @user_service_ns.marshal_with(user_return_fields)
    def get(self):
        '''List Users'''
        request_id =  common_utils.get_request_id()
        return_message = {constants.REQUEST_ID:request_id}
        try:

            self_logger = logger.bind(request_id=request_id, request_url=request.url)
            mobile_number = request.args.get(constants.MOBILE_NUMBER, None)
            otp = request.args.get(constants.OTP, None)
            try:
                otp = int(request.args.get(constants.OTP, None))
            except Exception as e:
                message = "invalid OTP:{}".format(otp)
                self_logger.error(message)
                return_message.update(message=message)
                common_utils.raise_exception(message, return_message, http.BAD_REQUEST.code)
            self_logger.info("given login parameters", mobile_number=mobile_number, otp=otp)
            if not mobile_number:
                message = "mobile number should not be empty"
                self_logger.error(message)
                return_message.update(message=message)
                common_utils.raise_exception(message, return_message, http.BAD_REQUEST.code)
            if not otp:
                message = "otp should not be empty"
                self_logger.error(message)
                return_message.update(message=message)
                common_utils.raise_exception(message,return_message, http.BAD_REQUEST.code)

            query = {constants.MOBILE_NUMBER: mobile_number, constants.OTP:otp}
            projection = {
                constants.MOBILE_NUMBER: 1,
                constants.OTP:1
            }
            self_logger.info("fetching user data", query=query, projection=str(projection))
            db_con_obj = DB(self_logger)
            data = db_con_obj.fetch_one(constants.USERS,query, projection=projection)
            self_logger = db_con_obj.logger
            if data:
                # create access_token and activate user
                access_token_creation_payload = {
                    constants.MOBILE_NUMBER: data[constants.MOBILE_NUMBER],
                    constants.OTP: data[constants.OTP],
                    constants._ID: data[constants._ID]
                }
                payload = {
                    #constants.OTP: "",
                    constants.IS_ACTIVE: True,
                    constants.ACCESS_TOKEN: common_utils.create_access_token(access_token_creation_payload)
                }

                return db_con_obj.find_one_update_or_create(constants.USERS, query, payload), 201
            else:
                message = "Invalid OTP"
                self_logger.info(message)
                return_message.update(message=message)
                common_utils.raise_exception(message, return_message, http.UNPROCESSABLE_REQUEST.code)
        except Exception as e:
            common_utils.process_resource_exception_block(self_logger, e, return_message)

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
        self_logger = logger.bind(request_id=request_id, request_url=request.url)
        try:
            '''Create User: full name,OTP and send OTP to registered mobile '''
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
                    payload[constants.OTP_EXPIRE_DATE] = common_utils.get_expired_date()
                else:
                    self_logger.info("token not expired", OTP=data[constants.OTP])
                    payload[constants.OTP] = data[constants.OTP]

            else:
                self_logger.info("user not registered previously", mobile_number=payload[constants.MOBILE_NUMBER])
                payload[constants.OTP] = common_utils.generate_otp()
                payload[constants.OTP_EXPIRE_DATE] = common_utils.get_expired_date()

            payload[constants.USER_TYPE] = constants.DEFAULT_USER
            payload[constants.USER_LOCATION] = []
            # send otp to mobile
            is_sms_send = common_utils.send_mobile_message(payload[constants.MOBILE_NUMBER])
            if  is_sms_send:
                self_logger.info("sms send successfully.", mobile_number = payload[constants.MOBILE_NUMBER])
                query = {constants.MOBILE_NUMBER: payload[constants.MOBILE_NUMBER]}
                created_doc = db_con_obj.find_one_update_or_create(constants.USERS,query, payload, True)
                self_logger.info("created document id {}".format(created_doc['_id']))
                return created_doc, http.SUCCESS.code
            message = "faild to send sms to:{mobile_number}".format(mobile_number = payload[constants.MOBILE_NUMBER])
            self_logger.error(message)
            return_message.update(message=message)
            common_utils.raise_exception(message,return_message, http.UNPROCESSABLE_REQUEST.code)
        except Exception as e:
            common_utils.process_resource_exception_block(self_logger, e, return_message)



@user_service_ns.route('/update-user-info')
class UpdateUserInfo(Resource):
    """
    It will creates user
    """
    @user_service_ns.errorhandler
    @helpers.check_access_token
    def post(self, *args, **kwargs):
        request_id = str(uuid.uuid4())
        return_message = {constants.REQUEST_ID:request_id}
        self_logger = logger.bind(request_id=request_id, request_url=request.url)
        try:
            '''Update User info: update user current location  '''
            update_payload = {}

            # kwargs should have decoded_token
            if constants.DECODED_TOKEN not in kwargs:
                message = "Token not found"
                self_logger.error(message)
                return_message.update(message=message)
                common_utils.raise_exception(message, return_message, http.UNAUTHORIZED.code)
            user_id = kwargs[constants.DECODED_TOKEN][constants._ID]
            original_payload = self.api.payload
            if constants.USER_LOCATION in original_payload and \
                    isinstance(original_payload[constants.USER_LOCATION], list) and \
                    len(original_payload[constants.USER_LOCATION]) == 2:

                update_payload.update({
                    constants.USER_LOCATION: original_payload[constants.USER_LOCATION],

                })
            else:
                message = "Invalid {} data:{}".format(constants.USER_LOCATION, original_payload[constants.USER_LOCATION])
                self_logger.error(message)
                return_message.update(message=message)
                common_utils.raise_exception(message, return_message, http.BAD_REQUEST.code)

            db_con_obj = DB(self_logger)
            query = {constants._ID: user_id}
            updated_doc = db_con_obj.find_one_update_or_create(constants.USERS, query, update_payload)
            if not updated_doc:
                message = "failed to update document"
                self_logger.error(message)
                return_message.update(message=message)
                common_utils.raise_exception(message, return_message, http.UNPROCESSABLE_REQUEST.code)
            return {
                       constants.MESSAGE: constants.DOCUMENT_UPDATED_SUCCESS,
                        constants.UPDATED_DATE: updated_doc[constants.UPDATED_DATE]
                    }, 200
        except Exception as e:
            common_utils.process_resource_exception_block(self_logger, e, return_message)
