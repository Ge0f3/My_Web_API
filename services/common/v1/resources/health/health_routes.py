import logging
import datetime
import time

from flask import request, abort, jsonify
from flask_restplus import Resource, Namespace

log = logging.getLogger(__name__)

ns = Namespace(
    'Health Check',
    description='Operations related to servic health')


@ns.route('')
class HealthCheck(Resource):
    def get(self):
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Origin': '*'},
            'body': "Everything looks Fine",
            'error': None}
