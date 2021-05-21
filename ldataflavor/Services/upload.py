import logging
import boto3
from botocore.exceptions import ClientError


def upload_file(user,file_name,tipo):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if tipo == 'image':
        object_name = "users/"+user+"/"+file_name
        print(object_name)
    

    # Upload the file
    bucket = 'to-vivo-app'
    s3_client = boto3.client('s3')
   # print(file_name, bucket, object_name,tipo)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        s3_url = "https://to-vivo-app.s3.amazonaws.com/"+object_name
        
    except ClientError as e:
        #logging.error(e)
        return False
    return s3_url
