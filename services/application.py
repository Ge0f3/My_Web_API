from flask import Flask
from importlib import import_module
from flask_bcrypt import Bcrypt
from werkzeug.contrib.fixers import ProxyFix
import decimal
import flask.json
import datetime
from bson.objectid import ObjectId
from services.blueprints import all_blueprints
import os
import json
import logging
import logging.config
from werkzeug.utils import cached_property


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


def setup_logging(
        default_path='logging_config.json',
        default_level=logging.INFO,
        env_key='LOG_CFG'):
    """
    Set up logging configuration for interaction service
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
        config['handlers']['error_file_handler']['filename'] = log_path + \
            error_filename

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def create_app(config_obg=None, **kwargs):
    app = Flask(__name__)
    setup_logging()
    print('Created app and set up logging!')

    register_blueprints(app)
    # https proxy
    app.wsgi_app = ProxyFix(app.wsgi_app)
    # custom json encoderd to deal with nonjson convertables
    app.json_encoder = MyJSONEncoder
    return app


def register_blueprints(app):
    for bp in all_blueprints:
        import_module(bp.import_name)
        app.register_blueprint(bp)
