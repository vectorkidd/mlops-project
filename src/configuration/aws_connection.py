import boto3
import os
from src.constants import AWS_ACCESS_KEY_ID_ENV_KEY, AWS_SECRET_ACCESS_KEY_ENV_KEY, REGION_NAME

class S3Client:

    s3_client = None
    s3_resource = None
    def __init__(self, region_name=REGION_NAME):

        __access_key_id = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
        __secret_access_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)

        if __access_key_id is None or __secret_access_key is None:
            raise ValueError("AWS access key ID and secret access key must be set in environment variables.")

        S3Client.s3_client = boto3.client('s3', region_name=region_name, aws_access_key_id=__access_key_id,
                                            aws_secret_access_key=__secret_access_key)
        S3Client.s3_resource = boto3.resource('s3', region_name=region_name, aws_access_key_id=__access_key_id,
                                            aws_secret_access_key=__secret_access_key)
        

