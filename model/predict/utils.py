import os
import boto3
import joblib


class Singleton:
    """Base class to make any class a singleton."""
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]
    

def get_secret_manager_value():
    client = boto3.client('secretsmanager')
    try:
        secret = client.get_secret_value(SecretId='my-db-password')
    except Exception as e:
        print(f"Error fetching secret from AWS Secrets Manager: {e}")
        raise

    return secret['SecretString']


def get_env_variable(var_name):
    try:
        value = os.getenv(var_name)
        if value is None:
            raise ValueError(f"Environment variable '{var_name}' is not set.")
        return value
    except Exception as e:
        print(f"Error retrieving environment variable '{var_name}': {e}")
        raise

def open_joblib_s3(s3_bucket, s3_key):
    # Read latest model from s3 bucket
    # Find date and time of latest model in s3 bucket

    s3_client = boto3.client('s3')

    try:
        s3_key = s3_client.list_objects_v2(Bucket=s3_bucket, Prefix=s3_key)['Contents'][-1]['Key']
    except Exception as e:
        print(f"Error fetching model from S3: {e}")
        raise

    try:
        s3_client.download_file(s3_bucket, s3_key, 'model.pkl')
    except Exception as e:
        print(f"Error downloading model from S3: {e}")
        raise
    
    try:
        model = joblib.load('model.pkl')
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        raise