from flask import Flask
from services.application import create_app
from services.config import RequiredConstants
from flask_restplus import Resource, Api

from flask_cors import CORS

import os
import logging

app = create_app()
api = Api(app)

# cross origin.
CORS(app, resources=r'/*')
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def testRoute():
    return '<h1> API service running! </h1>'


if __name__ == '__main__':
    app.run(debug=True, threaded=False, host='0.0.0.0', port=5000)
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
