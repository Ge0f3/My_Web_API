from flask_restplus import fields, Model


image_classification_schema=Model('Image classification schema',{
    'account_number': fields.String,
    'model_name': fields.String,
    's3_key': fields.String,
    'bucket_name': fields.String,
})

job_schema=Model('Job Request', {
    'job_id': fields.String,
    'service_name': fields.String,
    'payload': fields.Nested(image_classification_schema)
})



