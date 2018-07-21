import logging
import structlog
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

from .utils import constants
from .utils import config

#from es.elastic_client import im

mongo = PyMongo()
#qvd_es_client = QvdElasticClient(origin=constants.QVD_ORIGIN, timeout=constants.ES_TIMEOUT,
#                                max_retries=constants.ES_MAX_RETRIES, retry_on_timeout=constants.ES_RETRY_ON_TIMEOUT)

logger = structlog.get_logger()


def create_app(package_name, config_path=None,
               settings_override=None, env=None):
    """
    returns flask.Flask application instance with config_path configurations
     and with blueprint registered
    :param package_name: application name
    :param config_path: configuration module path
    :param settings_override: a dict of settings to overwrite
    :param env:
    :return: qvd-api application flask instance object
    """
    app = Flask(package_name, instance_relative_config=True)

    # configuration details getting and setting
    app.config.from_object(config_path)
    app.config.from_object(settings_override)

    # Logging
    if env != constants.LOCAL:
        gunicorn_err = logging.getLogger()
        # We want tracebacks to show up in the gunicorn error log, and we want to turn off
        # All other console output, so we completely  overwrite default/production (stderr) loggers
        # For all of our own log messages, we'll be using structlog. These will also
        # go to gunicorn's error handler.
        app.logger.handlers = gunicorn_err.handlers[:]
    # Connect extensions to application
    CORS(app)  # CORS for all routes

    # initalize mongo host
    mongo.init_app(app)

    # register blueprints
    from .apis import blueprint
    app.register_blueprint(blueprint)

    # It can sometimes be useful to know when the app was last started up
    logger.new().info("STARTED")
    return app

