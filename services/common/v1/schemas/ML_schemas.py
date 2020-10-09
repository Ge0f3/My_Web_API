from flask_restplus import fields, Model, reqparse
import werkzeug

spam = Model('spam Schema', {
    'text': fields.String,
})