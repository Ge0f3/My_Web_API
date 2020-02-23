from services.config import RequiredConstants as RC
import requests
import boto3
import datetime
import shutil
import PIL.Image as Image
import zipfile
import logging, json, os, pickle, shutil
from flask import request,jsonify
from services.core.Validation import Validation
from botocore.exceptions import ClientError
from werkzeug.datastructures import FileStorage

# dataset encoding methods
import chardet

#Data Processing
import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords, wordnet
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from wordcloud import STOPWORDS
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import WhitespaceTokenizer
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

#Algorithms
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB  
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn import svm

#Metrices
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder

#configuring s3 Access
s3= boto3.client("s3",aws_access_key_id = RC.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = RC.AWS_SECRET_ACCESS_KEY
    )

log = logging.getLogger(__name__)

USAGE_SERVICE = RC.USAGE_SERVICE

class ServiceLayer:

    @staticmethod
    def clean_directories(file_name):
        try:
            base_dir = os.path.join('./zip_downloads/')
            folder_name = file_name.split('.')[0]
            os.remove(base_dir + file_name)
            shutil.rmtree(base_dir + folder_name)
        except Exception as e:
            print(e)
            return e

    @staticmethod
    def train_nlp(payload, job_id, service_name):
        try:
            s3_key = payload.get('s3_key')
            zip_file_name = s3_key.split('/')[-1]

            folder_name = zip_file_name.split('.')[0]
            s3.download_file(RC.BUCKET_NAME,s3_key,'./zip_downloads/'+zip_file_name)

            my_zip_file = zipfile.ZipFile('./zip_downloads/'+zip_file_name, 'r')
            my_zip_file.extractall(path='./zip_downloads/'+folder_name)

            full_file_path = os.path.join('./zip_downloads', folder_name, payload.get('file_name'))

            file = FileStorage(open(full_file_path, 'rb'))

            ServiceLayer.perform_nlp(payload.get('form_data'), file, payload.get('account_number'))

            #make calls to Usage service and Queue service
            to_send_queue = {
                'job_id': job_id,
                'service_name': service_name,
                'status': 'finished',
            }
            #This should be a 200, 
            response_queue = requests.put(RC.QUEUE_SERVICE + '/v1/queue/job', json=to_send_queue)

            ServiceLayer.clean_directories(zip_file_name)

            log.info('Job update sent to quueue')
            log.info('Model meta data sent to usage service.')
            log.info('Training Complete')

        except Exception as e:
            log.error(e)
            print(e)
            to_send_queue = {
                'job_id': job_id,
                'service_name': service_name,
                'status': 'error',
            }
            #This should be a 200, 
            response_queue = requests.put(RC.QUEUE_SERVICE + '/v1/queue/job', json=to_send_queue)

    # @staticmethod
    # def determine_pos(word):
    #     tag = nltk.pos_tag([word])
    #     tag = tag[0][1]
    #     if tag.startswith('J'):
    #         return wordnet.ADJ
    #     elif tag.startswith('V'):
    #         return wordnet.VERB
    #     elif tag.startswith('N'):
    #         return wordnet.NOUN
    #     elif tag.startswith('R'):
    #         return wordnet.ADV
    #     else:
    #         return wordnet.NOUN

    @staticmethod
    def clean_text_values(column):
        # Make all text lowercase
        clean_text = column.apply(lambda x: str(x).lower())

        # Remove stopwords using joint NLTK and wordcloud stopwords
        eng_stop_words = set(stopwords.words('english')).union(set(ENGLISH_STOP_WORDS)).union(set(STOPWORDS))
        tweet_column = []
        
        # remove special characters, numbers, punctuations
        clean_text = clean_text.str.replace("[^a-zA-Z#]", " ")
        clean_text = clean_text.str.replace("http", " ")
        clean_text = clean_text.str.replace('#', '')

        # Remove unwanted text
        for query in clean_text:
            querywords = query.split()
            resultwords  = [word for word in querywords if word.lower() not in eng_stop_words]
            result = ' '.join(resultwords)
            tweet_column.append(result)  
        tokenizer = WhitespaceTokenizer()
        lemmatizer = WordNetLemmatizer()
    
        # return pd.Series(tweet_column).apply(lambda x: [lemmatizer.lemmatize(word, ServiceLayer.determine_pos(word)) for word in tokenizer.tokenize(x)])
        return pd.Series(tweet_column).apply(lambda x: [lemmatizer.lemmatize(word) for word in tokenizer.tokenize(x)])


    @staticmethod
    def nlp_modeling(df,label_column,text_column):
        # Start text preprocessing using df.apply and lambda exp
        df.apply(ServiceLayer.clean_text_values)

        countvect= CountVectorizer(ngram_range=(2,2),)
        corpus = countvect.fit(df[text_column].apply(lambda x: np.str_(x)))

        docterm_matrix = countvect.transform(df[text_column])
       
        df_labels= df[label_column]

        #splitting the test and train data
        trainset, testset, trainlabel, testlabel = train_test_split(docterm_matrix, df_labels, test_size=0.33, random_state=42, shuffle=True)

        #Declare model objects
        #Naive_bayes,DT,SVM,Linear regression,K-NN
        dtc = DecisionTreeClassifier()
        nbc = MultinomialNB()
        LR = LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial')
        # SVM = svm.LinearSVC(kernel='rbf', C=1,gamma='auto')
        knn = KNeighborsClassifier(n_neighbors=3)  
        print('objects for the model declared')

        # Training the model
        dtc.fit(trainset, trainlabel)
        nbc.fit(trainset, trainlabel)
        LR.fit(trainset, trainlabel)
        # SVM.fit(trainset, trainlabel)
        knn.fit(trainset, trainlabel)
        print('Model has been trained')

        #Predict the model
        dtc_predict= dtc.predict(testset)
        nbc_predict= nbc.predict(testset)
        lr_predict = LR.predict(testset)
        # svm_predict = SVM.predict(testset)
        knn_predict = knn.predict(testset)
        print('Predictions has been made from each model')

        #Model Evalutaion 
        accuracy = dict()
        accuracy['Naive_bayes']=accuracy_score(testlabel,nbc_predict)
        accuracy['DecisionTree'] = accuracy_score(testlabel, dtc_predict)
        # accuracy['support_vector_Machines'] = accuracy_score(testlabel,svm_predict)
        #This should be replaced with logisitic regression instead of linear regression 
        accuracy['Linear_Regressor'] = accuracy_score(testlabel,lr_predict)
        accuracy['KNN'] = accuracy_score(testlabel,knn_predict)
        print('Model has been evaluated')

        max_accuracy_algo = max(accuracy,key=accuracy.get)
        print('Max accuracy determined!\nMax accuracy model is {}'.format(max_accuracy_algo))
        print('Accuracy value is: ' + str(accuracy[max_accuracy_algo]))

        best_model = {
            'Naive_bayes':nbc,
            'DecisionTree':dtc,
            # 'support_vector_Machines':SVM,
            'Linear_Regressor':LR,
            'KNN':knn
        }[max_accuracy_algo]

        #Serializing and saving the model/document matrix with highest accuracy
        model = pickle.dumps(best_model)
        pickled_corpus = pickle.dumps(corpus)

        return model,max_accuracy_algo,accuracy[max_accuracy_algo], pickled_corpus

    @staticmethod
    def perform_nlp(form_data, file, account_number):
        print(form_data)
        columns = json.loads(form_data['columns'])
        try:
            test_val = json.loads(form_data['test'])
        except Exception as e:
            test_val = 0
        models_created = dict()
        print("Wizard data has been retrieved from the API request")

        #Columns selected by the user as feature
        selected_columns = [column['column_name'] for column in columns if column['keep'] is True] 

        #Model name for each label 
        model_name = str([column['model_name'] for column in columns if column['label'] is True][0])

        #Columns selected by the user as labels
        label_column = str([column['column_name'] for column in columns if column['label'] is True][0])

        # Text column name
        text_column = str([column['column_name'] for column in columns if (column['label'] is False and column['keep'] is True)][0])
        print("The labels are {}".format(label_column))
        
        # read data file as pandas dataframe
        # enc_dict = chardet.detect(file.stream.read())
        # best_enc = enc_dict['encoding']
        encoding=''
        try:
            df = pd.read_csv(file)
            encoding = 'utf-8'
        except Exception as e:
            # reset file iterator to re-read file
            file.seek(0)
            print('UTF-8 encoding not working, trying Latin-1')
            df = pd.read_csv(file, encoding='latin-1')
            encoding = 'latin-1'

        # By Default for NLPs discarding null values  
        drop_cols = set(list(df)).difference(set(selected_columns))
        df.drop(columns=drop_cols, inplace=True)
        df.dropna(inplace=True)
        print("Null values discarded")
        

        nltk.download('wordnet')
        nltk.download('stopwords')
        model,max_accuracy_algo,accuracy, corpus = ServiceLayer.nlp_modeling(df,label_column,text_column)

        #Replace classification with nlp 
        models_created[model_name]=[accuracy,'NLP']
        accuracy_value = accuracy
        accuracy_type = 'percent'

        #Storing the model with the account number in s3
        if test_val is 0:
            #uploading model  to s3 bucket 
            s3_response= s3.put_object(Body=model,Bucket=RC.BUCKET_NAME,Key=account_number+'/nlp/'+model_name)
            s3_matrix_resp = s3.put_object(Body=corpus,Bucket=RC.BUCKET_NAME,Key=account_number+'/nlp/'+model_name+'_corpus')
            #model information to usage api 
            to_send= {
                "account_number": account_number,
                "model_name":model_name,
                "accuracy_value": str(accuracy_value),
                "accuracy_type": accuracy_type,
                "property_cols":selected_columns,
                "label_col":label_column,
                "algorithm":max_accuracy_algo,
                "type":"NLP",
                "s3_folder": account_number+'/nlp/',
                "encoding": str(encoding),
                "latest_s3_id":s3_response['VersionId'],
                "files_uploaded": [{
                    "file_name": model_name ,
                    "date_uploaded" : datetime.datetime.now().isoformat(),
                    "active": True,
                    "date_deleted" : None,
                    "s3_id": s3_response['VersionId']}]
                }
            usage_api_response = requests.post(USAGE_SERVICE+"/v1/usage/models/"+account_number, json=to_send)
            print("Response send to the Usage API \n Response {}".format(usage_api_response))


        return models_created, df[label_column].value_counts().to_dict()
        
