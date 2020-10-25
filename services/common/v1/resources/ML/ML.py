import logging
from flask import request, jsonify
import requests
import json
import os
from services.config import RequiredConstants as RC
from flask_restplus import Resource, Namespace, reqparse
from services.common.v1.schemas.ML_schemas import spam, mpg ,iris
from services.common.v1.resources.ML.ServiceLayer import ServiceLayer


log = logging.getLogger(__name__)

ns = Namespace(
    'Machine Learning',
    description='Operation Realted to Machine learning Model API')
ns.models[spam.name] = spam
ns.models[mpg.name] = mpg
ns.models[iris.name] = iris


@ns.route('/spam')
class Spam(Resource):
    @ns.expect(spam)
    def post(self):
        form_data = request.json

        email = form_data['email']

        try:
            prediction = ServiceLayer.predict_spam(email)

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/plain',
                    'Access-Control-Allow-Origin': '*'},
                'body': prediction[0]}
        except Exception as E:
            log.error(E)
            return jsonify({'Error': "The error is {}".format(E)})

@ns.route('/spam_batch')
class SpamBatch(Resource):
    def post(self):
        form_data = request.files['file']
        log.info("File recieved")
        try:
            response = ServiceLayer.predict_spam_batch(form_data)

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/plain',
                    'Access-Control-Allow-Origin': '*'},
                'body': response}
        except Exception as E:
            log.error(E)
            return jsonify({'Error': "The error is {}".format(E)})


@ns.route('/mpg')
class MPG(Resource):
    @ns.expect(mpg)
    def post(self):
        form_data = request.json

        data = [int(form_data['cylinders']), int(form_data['displacement']), int(form_data['horepower']), int(form_data['weight']), int(form_data['acceleration']), int(form_data['model_year'])]
        if(form_data['Origin'] == 'USA'):
            data.extend([int(0), int(0), int(1)])
        elif(form_data['Origin'] == 'Europe'):
            data.extend([int(0), int(1), int(0)])
        elif(form_data['Origin'] == 'Japan'):
            data.extend([int(1), int(0), int(0)])

        try:
            print(data)
            prediction = ServiceLayer.predict_mpg(data)

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/plain',
                    'Access-Control-Allow-Origin': '*'},
                'body': prediction}
        except Exception as E:
            log.error(E)
            return jsonify({'Error': "The error is {}".format(E)})


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


@ns.route('/iris')
class iris(Resource):
    @ns.expect(iris)
    def post(self):
        form_data = request.json

        data = [float(form_data['sepal_length']), float(form_data['petal_length']),  float(form_data['petal_width'])]
        print(data)
        try:
            prediction = ServiceLayer.predict_iris(data)
            print(prediction)
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/plain',
                    'Access-Control-Allow-Origin': '*'},
                'body': prediction}
        except Exception as E:
            log.error(E)
            return jsonify({'Error': "The error is {}".format(E)})
