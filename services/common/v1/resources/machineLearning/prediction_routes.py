import logging
from flask import request,jsonify
import json 
from flask_restplus import Resource, Namespace, reqparse
from werkzeug.datastructures import FileStorage
from services.common.v1.resources.machineLearning.ServiceLayer import ServiceLayer
from services.common.v1.schemas.image_classification_schemas import image_classification_schema


log = logging.getLogger(__name__)

ns = Namespace('ML', description='ML Model API"s')


parser = reqparse.RequestParser()
parser.add_argument('file', location='files', type=FileStorage)
parser.add_argument('path')



@ns.route('/predict')
class PredictModel(Resource):
    def post(self):
        '''upload dataset to get prediction from the trained ML model'''
        try:
            print("post method")
            email = request.form['email']
            if email:
                prediction= ServiceLayer.predict(email)
                
                return jsonify({
                    'Prediction':prediction[0]
                })
            else:
                return jsonify({
                    "Error":"File not Supported"
                })

        except Exception as E:
            print(E)
            log.error(E)
            return jsonify({'Error':"The error is {}".format(E)})
        
        

       
