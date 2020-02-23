import logging
from flask import request
from flask_restplus import Resource, Namespace, reqparse
from werkzeug.datastructures import FileStorage
from services.common.v1.resources.deepLearning.ServiceLayer import ServiceLayer
from services.common.v1.schemas.nlp_schemas import nlp_schema, job_schema
from services.utils.Compute import Compute

log = logging.getLogger(__name__)

ns = Namespace('DL', description='DL Model API"s')

ns.models[nlp_schema.name]=nlp_schema
ns.models[job_schema.name]=job_schema

# function to run in thread
def runCompute(payload, job_id, service_name):
    result = ServiceLayer.train_nlp(payload, job_id, service_name)
    print(result)
    return True


@ns.route('/perform_nlp')
class PerformNlp(Resource):
    def post(self):
        try: 
            '''Perform NLP with a user-specified dataset'''
            print('Received request!')

            file = request.files['file']
            data = request.form
            models_created, value_counts = ServiceLayer.perform_nlp(data, file)

            print('Model has been created')
            response = {
                "models":models_created,
                "value_counts": value_counts
            }
            return jsonify(response)

        except Exception as E:
            print(E)
            return jsonify({'Error':"The error is {}".format(E)})
        

@ns.route('/train')
class Upload(Resource):
    @ns.expect(job_schema)
    def post(self):
        '''Provide image directory to train the natural langauge processing model'''
        try:
            log.debug('Training a natural langauge processing model with ')

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