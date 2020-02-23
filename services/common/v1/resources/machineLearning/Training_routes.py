import logging
from flask import request
import pickle
from flask_restplus import Resource, Namespace, reqparse
from werkzeug.datastructures import FileStorage
from services.common.v1.resources.machineLearning.ServiceLayer import ServiceLayer
from services.common.v1.schemas.image_classification_schemas import image_classification_schema, job_schema
from services.utils.Compute import Compute

log = logging.getLogger(__name__)

ns = Namespace('ML', description='ML Model funtions')
ns.models[image_classification_schema.name]=image_classification_schema
ns.models[job_schema.name]=job_schema

parser = reqparse.RequestParser()
parser.add_argument('file', location='files', type=FileStorage)
parser.add_argument('path')


# function to run in thread
def runCompute(payload, job_id, service_name):
    result = ServiceLayer.train_neural_network(payload, job_id, service_name)
    print(result)
    return True

@ns.route('/train')
class Upload(Resource):
    @ns.expect(job_schema)
    def post(self):
        '''Provide image directory to train the image classification model'''
        try:
            log.debug('Training a image classification model with ')

            data = request.json

            payload = data['payload']
            job_id = data['job_id']
            service_name = data['service_name']
            #loss, acc, val_loss,val_acc = ServiceLayer.train_neural_network(image_folder)

            # Run actual image training in seperate thread.
            myThread = Compute(runCompute, { 'payload': payload, 'job_id': job_id, 'service_name': service_name} )
            myThread.start()

            # Returns True, 200 to ackowledge that training has started
            result = True
            log.debug('Training Started !')
            return "{}".format(result), 200


        except Exception as E:
            print(E)
            return E
        
