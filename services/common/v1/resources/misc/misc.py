import logging
import datetime
import time

from flask import request, abort, jsonify
from flask_restplus import Resource, Namespace
from services.common.v1.schemas.ML_schemas import send_email
from services.common.v1.resources.misc.ServiceLayer import ServiceLayer
from services.config import RequiredConstants as RC

log = logging.getLogger(__name__)

ns = Namespace(
    "Misc API's",
    description="API's related to misc servic ")
ns.models[send_email.name] = send_email


@ns.route('/send_email')
class SendEmail(Resource):
    @ns.expect(send_email)
    def post(self):
        form_data = request.json
        try:
            response = ServiceLayer.send_email(form_data)
            print(response)
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/plain',
                    'Access-Control-Allow-Origin': '*'},
                'body': 'Success'}
        except Exception as E:
            log.error(E)
            return jsonify({'Error': "The error is {}".format(E)})
