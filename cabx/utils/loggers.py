import datetime
import uuid
import logging
from flask import request
from pythonjsonlogger import jsonlogger

from . import constants

def add_app_name(logger, log_method, event_dict):  # pragma: no cover
    event_dict["application"] = constants.APPLICATION_NAME
    return event_dict

def add_request_id(logger, log_method, event_dict):  # pragma: no cover
    event_dict['request_id'] = str(uuid.uuid4())
    return event_dict

class JsonLogFormatter(jsonlogger.JsonFormatter):  # pragma: no cover
    def add_fields(self, log_record, record, message_dict):
        """
        This method allows us to inject custom data into resulting log messages
        """
        for field in self._required_fields:
            log_record[field] = record.__dict__.get(field)
        log_record.update(message_dict)

        # Add timestamp and application name if not present
        if "timestamp" not in log_record:
            now = datetime.datetime.now()
            log_record["timestamp"] = datetime.datetime.strftime(now, format=constants.LOGGING_TS_FORMAT)

        if "application" not in log_record:
            log_record["application"] = constants.APPLICATION_NAME

        for field in log_record:
            if log_record[field] is not None:
                log_record[field] = str(log_record[field])
            else:
                log_record[field] = ""

        # message field returns null every time so remove it, if exists
        log_record.pop("message", None)
        jsonlogger.merge_record_extra(record, log_record, reserved=self._skip_fields)


#ATTR_TO_JSON = ['created', 'filename', 'funcName', 'levelname', 'lineno', 'module', 'msecs', 'msg', 'name', 'pathname', 'process', 'processName', 'relativeCreated', 'thread', 'threadName']
ATTR_TO_JSON = ['msg', 'levelname', 'lineno']
class TextFormatter(logging.Formatter):
    def format(self, record, *args, **kwargs):
        """
        construct custom text log messages to easy understand purpose.
        :param record:
        :param args:
        :param kwargs:
        :return:
        """
        method = ""
        url = ""
        record = {attr: getattr(record, attr) for attr in ATTR_TO_JSON}
        if constants.REQUEST_METHOD in dir(request):
            method = request.method
        if constants.REQUEST_URL in dir(request):
            url = request.url
        #return str(record)
        message_format = '{timestamp} {levelname}  {method}   {url}   "{message}"'
        record_msg = record['msg']
        request_id = record_msg.get(constants.REQUEST_ID, "")
        message = message_format.format(timestamp=record_msg['timestamp'], method=method, url=url,
                                        message=record_msg['event'], levelname=record['levelname']
                                        )
        if request_id:
            message += " request_id={}".format(request_id)
        return message