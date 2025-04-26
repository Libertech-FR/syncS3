from cn_s3_api.api import CNS3Api
from  utils import config
import os
def connect_s3():
    s3_api =  CNS3Api(dict(
        aws_access_key_id=config.get_key(config.get_section(), 'access_key'),
        aws_secret_access_key=config.get_key(config.get_section(), 'secret_key'),
        endpoint_url=config.get_key(config.get_section(), 'end_point'),
        region_name=config.get_key(config.get_section(), 'region'),
    ))
    return s3_api
def copy_to_s3(file):
    s3_api = connect_s3()
    filename=os.path.basename(file)
    s3path=config.get_key(config.get_section(),'dir_dest') + "/" + filename
    try:
    	s3_api.upload_file(config.get_key(config.get_section(),'bucket'), file, s3path)
    except Error:
        print("Erreur")

def delete_to_s3(file):
    s3_api = connect_s3()
    filename = os.path.basename(file)
    s3path = config.get_key(config.get_section(), 'dir_dest') + "/" + filename
    try:
    	s3_api.remove(config.get_key(config.get_section(),'bucket'),s3path)
    except Error:
        print("Erreur")

def list_s3(dir):
    s3_api = connect_s3()
    return s3_api.list(config.get_key(config.get_section(),'bucket'),dir)