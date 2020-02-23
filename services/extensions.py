from services.config import RequiredConstants as RC
import pymongo
from pymongo import MongoClient

import boto3

mongo = MongoClient(RC.MONGODB_URI)
mongodb = mongo[RC.MONGODB_DB]

S3 = boto3.client("s3",
    aws_access_key_id = RC.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = RC.AWS_SECRET_ACCESS_KEY
)