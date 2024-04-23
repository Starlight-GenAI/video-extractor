import json
import os
from google.cloud import storage
from config.config import  config
from adapter.auth import credentials, project_id

storage_client = storage.Client(project=project_id, credentials=credentials)
bucket = storage_client.bucket(config.cloud_storage.bucket_name)

def create_and_upload(subtitle, object_name):
    object_with_subfix = f'{object_name}.json'
    data = {'subtitle': subtitle}
    try:
        with open(object_with_subfix, 'w') as f:
            json.dump(data, f)
        upload(object_with_subfix)
    except Exception as e:
        raise e
        

def upload(object_name):
    try:
        blob = bucket.blob(object_name)
        blob.upload_from_filename(object_name)
        os.remove(object_name)
        # with open(object_name, 'rb') as f:
        #     file_obj = io.BytesIO(f.read())
        #     file_obj.seek(0)
        #     blob.upload_from_file(file_obj)
    except Exception as e:
        raise e
