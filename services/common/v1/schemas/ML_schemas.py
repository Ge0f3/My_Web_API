from flask_restplus import fields, Model, reqparse
import werkzeug

spam = Model('spam Schema', {
    'email': fields.String,
})

mpg = Model('AutoMPG Schema', {
    'cylinders': fields.String,
    'displacement': fields.String,
    'horepower': fields.String,
    'weight': fields.String,
    'acceleration': fields.String,
    'model_year': fields.String,
    'Origin': fields.String

})
