
"""
This is the people module and supports all the ReST actions for the
PEOPLE collection
"""

# System modules
from datetime import datetime


# 3rd party modules
from flask import make_response, abort
import connexion
import pickle
import pandas as pd
import numpy as np 
from flask import jsonify , request, Flask, render_template,redirect,url_for,send_file
from werkzeug.utils import secure_filename
from werkzeug import SharedDataMiddleware


#loading the models to the appplication
myPredict = pickle.load(open('./Models/model_file', 'rb'))
ser_countvect = pickle.load(open('./Models/countvect', 'rb'))


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API
PEOPLE = {
   "user_input1": {
        "email": "hi My name is xvasdfasdf",
    },
    "user_input2": {
        "email": "you won $1000 call 2312312 to win your option to grab this money",
    },
    "user_input3": {
        "email": "you havent paid your tax we are from xyz department sent",
    },
}


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    return [PEOPLE[key] for key in sorted(PEOPLE.keys())]


def read_one(lname):
    """
    This function responds to a request for /api/people/{lname}
    with one matching person from people
    :param lname:   last name of person to find
    :return:        person matching last name
    """

    
    # Does the person exist in people?
    if lname in PEOPLE:
        person = PEOPLE.get(lname)

    # otherwise, nope, not found
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )

    return person


def create(person):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    productname = person.get("email", None)
    product = [productname]
    x_count = ser_countvect.transform(product)

    # encode the json object to one hot encoding so that it could fit our model
    # get the  prediction

    res = myPredict.predict(x_count)

    # return a json value

    #app.logger.info('The type of the producname is {}'.format(res))
    return jsonify({'result': res[0]})
    # Does the person exist already?

    # Otherwise, they exist, that's an error
    
def update(lname, person):
    """
    This function updates an existing person in the people structure
    :param lname:   last name of person to update in the people structure
    :param person:  person to update
    :return:        updated person structure
    """
    # Does the person exist in people?
    if lname in PEOPLE:
        PEOPLE[lname]["fname"] = person.get("fname")
        PEOPLE[lname]["timestamp"] = get_timestamp()

        return PEOPLE[lname]

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )


def delete(lname):
    """
    This function deletes a person from the people structure
    :param lname:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the person to delete exist?
    if lname in PEOPLE:
        del PEOPLE[lname]
        return make_response(
            "{lname} successfully deleted".format(lname=lname), 200
        )

    # Otherwise, nope, person to delete not found
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )