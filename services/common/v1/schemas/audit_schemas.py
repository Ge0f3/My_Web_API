from flask_restplus import fields, Model

audit_schema = Model('Audit', {
    'audit_id': fields.String,
    'year_month': fields.String,
    'created_at': fields.String,
    'body': fields.Raw
})

new_audit_schema = Model('New Audit Schema', {
    'body': fields.Raw
})
