from flask_restplus import fields, Model


nlp_schema=Model('NLP schema',{
    'account_number': fields.String,
    'model_name': fields.String,
    's3_key': fields.String,
    'bucket_name': fields.String,
    'form_data': fields.Raw,
})

job_schema=Model('NLP Job Request', {
    'job_id': fields.String,
    'service_name': fields.String,
    'payload': fields.Nested(nlp_schema)
})



