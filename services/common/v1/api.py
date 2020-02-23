import logging

from flask_restplus import Api

from services.blueprints import common_blueprint_v1

from services.common.v1.resources.machineLearning.Training_routes import ns as ml_routes
from services.common.v1.resources.machineLearning.prediction_routes import ns as prediction_routes
from services.common.v1.resources.deepLearning.nlp_wizard import ns as dl_routes
from services.common.v1.resources.health.health_routes import ns as health_routes

log = logging.getLogger(__name__)

api = Api(common_blueprint_v1,
          version='1.0',
          title='My Web ML and Deep learning Model API',
          description='description for api')

# prefixes
ML = '/ML'
DL = '/DL'
health = '/health'

api.add_namespace(ml_routes, path=ML)
api.add_namespace(prediction_routes,path=ML)
api.add_namespace(health_routes, path=health)
api.add_namespace(dl_routes, path=DL)

