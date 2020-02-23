from flask import Flask
from importlib import import_module

from services.config import RequiredConstants
from services.blueprints import all_blueprints
from flask_bcrypt import Bcrypt
import decimal
import flask.json
import datetime
from bson.objectid import ObjectId
import os, json, logging, logging.config
from services.common.v1.resources.machineLearning.ServiceLayer import ServiceLayer as SL
# [END imports]

class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(MyJSONEncoder, self).default(obj)

def setup_logging(default_path='logging_config.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    Setup logging configuration
    """

    path = default_path
    value = os.getenv(env_key, None)
    log_path = os.getenv('LOG_LOCATION', '')

    if value:
        path = value

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)

        
        info_filename = config['handlers']['info_file_handler']['filename']
        error_filename = config['handlers']['error_file_handler']['filename']

        config['handlers']['info_file_handler']['filename'] = log_path + info_filename
        config['handlers']['error_file_handler']['filename'] = log_path + error_filename
        
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

app = Flask(__name__)
bcrypt = Bcrypt(app)

def load_models():
    print("<------------------- loading ML models and starting Flask server ----------------->")
    SL.load_auto_mpg()
    SL.load_ham_spam()
    print("<------------------- ML models loaded ----------------->")

def create_app(config_obj=None, **kwargs):
    setup_logging()
    if config_obj:
        app.config.from_object(config_obj)
    else:
        app.config.from_object(RequiredConstants)

    register_blueprints(app)

    #Loading Models before starting the app
    load_models()
    #custom json encoderd to deal with nonjson convertables
    app.json_encoder = MyJSONEncoder
    return app


def register_blueprints(app):
    for bp in all_blueprints:
        import_module(bp.import_name)
        app.register_blueprint(bp)
