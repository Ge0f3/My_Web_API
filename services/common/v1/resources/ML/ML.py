import logging
from flask import request, jsonify
import requests
import json
import os
from services.config import RequiredConstants as RC
from flask_restplus import Resource, Namespace, reqparse
from services.common.v1.schemas.ML_schemas import spam
from services.common.v1.resources.ML.ServiceLayer import ServiceLayer


log = logging.getLogger(__name__)

ns = Namespace(
    'Machine Learning',
    description='Operation Realted to Machine learning Model API')
ns.models[spam.name] = spam


@ns.route('/spam')
class Spam(Resource):
    @ns.expect(spam)
    def post(self):
        form_data = request.form

        result = form_data['text']

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Origin': '*'},
            'body': result}


@ns.route('/mpg')
class MPG(Resource):
    @ns.expect(spam)
    def post(self):
        form_data = request.form

        result = form_data['text']

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Origin': '*'},
            'body': result}


@ns.route('/house_price')
class HousePrice(Resource):
    def post(self):
        form_data = request.form

        result = form_data['text']
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Origin': '*'},
            'body': result}
