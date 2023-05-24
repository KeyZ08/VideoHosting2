import os

import boto3
from dotenv import load_dotenv

from users.CastomException import DisplayedException

dotenv_path = os.path.join(os.path.dirname(__file__), '../vk_cloud.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

ENDPOINT_URL = os.getenv('ENDPOINT_URL')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
SERVICE_NAME = os.getenv('SERVICE_NAME')


def get_vkClient():
    s3_client = boto3.session.Session().client(
        service_name=SERVICE_NAME,
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    return s3_client


def upload_file_with_callback(file, path, callback):
    client = get_vkClient()
    client.upload_fileobj(file, AWS_STORAGE_BUCKET_NAME, path, Callback=callback)


def delete_object(file_path):
    print(file_path)
    client = get_vkClient()
    client.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=file_path, )


def load(file, path):
    try:
        upload_file_with_callback(file, path, callback=None)
    except Exception as e:
        print(e)
        raise DisplayedException("Не удалось загрузить файл")