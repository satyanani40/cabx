from flask import Blueprint
from flask_restplus import Api

from feqor.utils import constants

blueprint = Blueprint('api', __name__,  url_prefix='/api')
api = Api(blueprint,
          version=constants.VERSION,
          title=constants.APPLICATION_NAME,
          description=constants.DESCRIPTION
)

from .mongo_metrics.mongo_metrics import mongodb_metrics_ns
api.add_namespace(mongodb_metrics_ns)