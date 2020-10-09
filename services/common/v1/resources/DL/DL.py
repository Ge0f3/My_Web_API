import logging
from flask import request, jsonify
import requests
import json
import os
from services.config import RequiredConstants as RC
from flask_restplus import Resource, Namespace, reqparse
from services.common.v1.schemas.ML_schemas import spam
from services.common.v1.resources.DL.ServiceLayer import ServiceLayer

log = logging.getLogger(__name__)

ns = Namespace(
    'DeepLearning',
    description='Operation Realted to Deep learning Model API')
ns.models[spam.name] = spam


@ns.route('/mnsit')
class mnsit(Resource):
    @ns.expect(spam)
    def post(self):
        form_data = request.form
        app.logger.info("MINST API ")
        result = form_data['text']

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Origin': '*'},
            'body': result}

@ns.route('/img_recog')
class Img_Recog(Resource):
    @ns.expect(spam)
    def post(self):
        form_data = request.form
        app.logger.info("MINST API ")
        result = form_data['text']

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Origin': '*'},
            'body': result}
