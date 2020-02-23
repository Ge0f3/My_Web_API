from services.config import RequiredConstants as RC
import requests
import boto3
import os
import datetime
import shutil
import PIL.Image as Image
import io
import pickle
import zipfile
import logging
from flask import request,jsonify
from tensorflow import keras
from services.core.Validation import Validation
from botocore.exceptions import ClientError

import numpy as np 
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import backend as K
tf.logging.set_verbosity(tf.logging.ERROR)

log = logging.getLogger(__name__)

s3= boto3.client(
    "s3",
    aws_access_key_id = RC.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = RC.AWS_SECRET_ACCESS_KEY
)


class ServiceLayer:
    @staticmethod
    def clean_directories(file_name, file_name_2):
        try:
            base_dir = os.path.join('./zip_downloads/')
            folder_name = file_name.split('.')[0]
            os.remove(base_dir + file_name)
            os.remove(base_dir + file_name_2)
            shutil.rmtree(base_dir + folder_name)
        except Exception as e:
            print(e)
            return e
    
    @classmethod
    def load_ham_spam(cls):
        global ham_spam 
        ham_spam = pickle.load(open('./Models/model_file','rb'))
        global ham_spam_xcount 
        ham_spam_xcount= pickle.load(open('./Models/countvect','rb'))
        print("ham spam model loaded !!!")

    @classmethod
    def load_auto_mpg(cls):
        global auto_mpg 
        auto_mpg= pickle.load(open('./Models/auto_mpg','rb'))
        print("AutoMPG model Loaded !!!")
    

    @classmethod
    def predict(cls,email):
        xcount = ham_spam_xcount.transform([email])
        prediction = ham_spam.predict(xcount)
        return prediction
    
    @staticmethod
    def create_neural_network_model(label_count):
        try:
            #Createing the neural network 
            model = tf.keras.models.Sequential([
                    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
                    tf.keras.layers.MaxPooling2D(2, 2),

                    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
                    tf.keras.layers.MaxPooling2D(2,2),
                    
                    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
                    tf.keras.layers.MaxPooling2D(2,2),
                
                    tf.keras.layers.Flatten(),

                    tf.keras.layers.Dense(512, activation='relu'),
                    tf.keras.layers.Dense(label_count, activation='softmax')
                ])
            #Defining the optimizer and loss function for the model 
            model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
            return model 
            
        except Exception as E:
            return E

    @staticmethod
    def train_model(model,train_data_gen):
        try:
            EPOCHS=10
            BATCH_SIZE = 100 
            history = model.fit_generator(
                train_data_gen,
                steps_per_epoch=20,
                epochs=EPOCHS
            )
            return history
        except Exception as E:
            return E
        

    @staticmethod
    def train_neural_network(payload, job_id, service_name):
        try:
            s3_key = payload.get('s3_key')
            zip_file_name = s3_key.split('/')[-1]
            #unzip the imagefolder
            train_dir, labels = ServiceLayer.get_directories(s3_key, zip_file_name)

            #Get base image zip from s3, make the train and validation image sets from it
            
            BATCH_SIZE = 100  # Number of training examples to process
            IMG_SHAPE  = 150  # The Image shape after image pre-processing 
            train_image_generator = ImageDataGenerator(
                rescale=1./255,
                rotation_range=40,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                horizontal_flip=True,
                fill_mode='nearest'
            )  # Generator for our training data

            #validation_image_generator = ImageDataGenerator(rescale=1./255)

            #Image Pre-processing stage
            train_data_gen = train_image_generator.flow_from_directory(
                batch_size=BATCH_SIZE, 
                directory=train_dir, 
                shuffle=True, 
                target_size=(IMG_SHAPE,IMG_SHAPE), #(150,150) 
                class_mode='binary'
            )

            # val_data_gen = validation_image_generator.flow_from_directory(
            #     batch_size=BATCH_SIZE, 
            #     directory=validation_dir,
            #     shuffle=False,
            #     target_size=(IMG_SHAPE,IMG_SHAPE), #(150,150)
            #     class_mode='binary'
            # )
            
            #Creating the Neural Network architecture
            model = ServiceLayer.create_neural_network_model(len(labels))
            log.info("The model is {}".format(model.summary()))

            #Training the Neural Network with train data and testing it with validation dataset
            history = ServiceLayer.train_model(model,train_data_gen)

            model_name = payload.get('model_name', 'trained_model')
            model_file_name = model_name + '.h5'
            account_number = payload.get('account_number', '1234567890')
            #Saving the model 
            model.save( './zip_downloads/' + model_file_name )

            log.info("Model saved to disk")

            upload_filename = './zip_downloads/' + model_file_name
            upload_bucket = RC.BUCKET_NAME
            upload_key = '{}/Image/{}'.format(account_number, model_file_name)

            log.info(upload_filename,upload_bucket,upload_key )

            s3_response = s3.upload_file(
                Filename= upload_filename,
                Bucket=RC.BUCKET_NAME,
                Key=upload_key,
            )

            log.info(s3_response)

            # Clear tensorflow session to stop memory leak
            K.clear_session()

            log.info('Done with local files.')

            # Clean up\
            ServiceLayer.clean_directories(zip_file_name, model_file_name)

            #make calls to Usage service and Queue service
            to_send_queue = {
                'job_id': job_id,
                'service_name': service_name,
                'status': 'finished',
            }
            #This should be a 200, 
            response_queue = requests.put(RC.QUEUE_SERVICE + '/v1/queue/job', json=to_send_queue)

            log.info('Job update sent to quueue')

            #send model informaiton to Usage setvice
            to_send_usage = {
                'account_number': account_number,
                'model_name':model_name,
                "accuracy_value": str(history.history['acc'][9]), #9 due to us running 10 epochs
                "accuracy_type": 'percent',
                'algorithm':'Neural Network',
                'type':'Image',
                #'history':history,
                'labels': labels,
                's3_folder': account_number+'/Image/',
                #'latest_s3_id':s3_response['VersionId'],
                'files_uploaded': [{
                    'file_name': model_file_name,
                    'date_uploaded' : datetime.datetime.now().isoformat(),
                    'active': True,
                    'date_deleted' : None,
                    #'s3_id': s3_response['VersionId']
                }]
            }
            usage_api_response = requests.post(RC.USAGE_SERVICE+"/v1/usage/models/"+account_number, json=to_send_usage)

            log.info('Model meta data sent to usage service.')
            
            log.info('Training Complete')

            return "Training completed !!"

        except Exception as E:
            return E

    @staticmethod
    def predict_results(image, account_number, data):

        model_name = data.get('model_name', None)

        if not model_name or not account_number:
            return 'Error'
            
        s3_key = account_number + '/Image/' + model_name
        folder = './zip_downloads/'

        try:
            log.info('Loading the saved neural network')
            
            s3.download_file(RC.BUCKET_NAME, s3_key, folder + account_number + model_name)

            log.info("model downloaded")
            model = keras.models.load_model(folder + account_number + model_name)
            print(model.summary())

            log.info('Loading the saved neural network')
            IMG_SHAPE  = 150 
            log.info("loading the image")
            image_bytes = io.BytesIO(image)
            image_pil = Image.open(image_bytes)
            if image_pil.mode != "RGB":
                image_pil = image_pil.convert("RGB")
            image_pil = image_pil.resize((IMG_SHAPE,IMG_SHAPE))
            log.info("resizing the image")
            image_np = np.array(image_pil)/255.0

            image_bytes.close()
            image_pil.close()

            # Return the processed image
            log.info(image_np.shape)

            log.info("Predicting the image")
            prediction = model.predict(image_np[np.newaxis, ...])

            # Clear tensorflow session to stop memory leak
            K.clear_session()

            prediction = prediction.tolist()
            log.info('prediction Made {}'.format(prediction))

            #Remove model file after done using it.
            os.remove(folder + account_number + model_name)

            return prediction

        except Exception as E:
            print(E)
            return E



