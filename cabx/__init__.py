"""
feqor-api flask restplus application
"""
import logging.config
import os
import structlog


from .utils import loggers
from .utils import constants

__version__ = constants.VERSION
ENVIRONMENT = os.getenv("ENVIRONMENT")

structlog.configure(
    processors=[
        loggers.add_app_name,
        #loggers.add_request_id,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt=constants.LOGGING_TS_FORMAT),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        # structlog.processors.JSONRenderer()  # Not necessary because it gets formatted at a higher level
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

if ENVIRONMENT is not None and ENVIRONMENT == constants.LOCAL:  # pragma: no cover
    # This is completely unnecessary: just fancy coloring for local development logging.
    # It also fails to properly format one of the Flask default messages so you'll see
    # a Traceback for that message on startup!
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colors": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=True),
                "foreign_pre_chain": [structlog.stdlib.add_log_level,
                                      structlog.processors.TimeStamper(fmt=constants.LOGGING_TS_FORMAT)]
            }
        },
        "handlers": {
            "default": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "colors",
            }
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": "DEBUG",
                "propagate": True,
            },
        }
    })
