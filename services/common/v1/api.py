import logging
from flask_restplus import Api

from services.blueprints import common_blueprint_v1

from services.common.v1.resources.ML.ML import ns as ML
from services.common.v1.resources.DL.DL import ns as DL
from services.common.v1.resources.health.health_routes import ns as health_routes
from services.common.v1.resources.misc.misc import ns as misc

log = logging.getLogger(__name__)

api = Api(common_blueprint_v1,
          version='1.0',
          title='My Web APIs',
          description='Service that handles processing user input and sending back response')

# prefixes
MachineLearning = '/ml'

DeepLearning = '/dl'

Misc = '/misc'

health = '/health'

api.add_namespace(ML, path=MachineLearning)
api.add_namespace(DL, path=DeepLearning)
api.add_namespace(health_routes, path=health)
api.add_namespace(misc, path=Misc)
