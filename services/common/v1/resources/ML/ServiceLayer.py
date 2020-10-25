
import requests
import json
from flask import request
import pickle
import os
import numpy as np
import pandas as pd

parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

ham_spam = pickle.load(open('./Models/model_file', 'rb'))
xcount = pickle.load(open('./Models/countvect', 'rb'))

auto_mpg = pickle.load(open('./Models/auto_mpg', 'rb'))
iris = pickle.load(open('./Models/iris','rb'))


class ServiceLayer:

    @staticmethod
    def predict_spam(email):
        # To verify the email
        xcounts = xcount.transform([email])
        prediction = ham_spam.predict(xcounts)
        return prediction

    @staticmethod
    def predict_mpg(data):
        prediction = auto_mpg.predict([data])
        print(prediction)
        return prediction[0]
    
    @staticmethod
    def predict_iris(data):
        prediction = iris.predict([data])
        print(prediction[0])
        return prediction[0]

    @staticmethod
    def predict_spam_batch(form_data):
        df = pd.read_csv(form_data)
        df_tf = xcount.transform(df.text)
        prediction = ham_spam.predict(df_tf)
        df['Prediction'] = pd.Series(prediction).values
        value_counts = df['Prediction'].value_counts().to_dict()
        df = df.to_json(orient='records')
        df = json.loads(df)
        response = {
            'value_counts': value_counts,
            'result': df
        }
        return response
