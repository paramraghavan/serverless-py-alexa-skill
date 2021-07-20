from pathlib import Path
import os
import boto3

def get_boto3_client(aws_access_key_id, aws_secret_access_key, service='s3'):
    session = boto3.session.Session()
    return session.client(service_name=service,
                          region_name='us-east-1',
                          aws_access_key_id= aws_access_key_id,
                          aws_secret_access_key= aws_secret_access_key)
