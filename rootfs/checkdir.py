import os.path
from cn_s3_api.api import CNS3Api
import argparse
import configparser
import logging


__CONFIG__=configparser.RawConfigParser()
__SECTION__=''
def read_config(file):
    with open(file) as f:
        file_content = f.read()
    __CONFIG__.read_string(file_content)
    return __CONFIG__

def config(section,key,default=''):
    c=__CONFIG__[section]
    return c.get(key,default)

def get_config():
    items=__CONFIG__.items('config')
    data = {}
    for k, v in items:
        data[k] = v
    return data

def connect_s3():
    s3_api = CNS3Api(dict(
        aws_access_key_id=config(__SECTION__, 'access_key'),
        aws_secret_access_key=config(__SECTION__, 'secret_key'),
        endpoint_url=config(__SECTION__, 'end_point'),
        region_name=config(__SECTION__, 'region'),
    ))
    return s3_api
def copy_to_s3(file):
    s3_api = connect_s3()
    filename=os.path.basename(file)
    s3path=config(__SECTION__,'dir_dest') + "/" + filename
    try:
    	s3_api.upload_file(config(__SECTION__,'bucket'), file, s3path)
    except Error:
        print("Erreur")

def delete_to_s3(file):
    s3_api = connect_s3()
    filename = os.path.basename(file)
    s3path = config(__SECTION__, 'dir_dest') + "/" + filename
    try:
    	s3_api.remove(config(__SECTION__,'bucket'),s3path)
    except Error:
        print("Erreur")

def list_s3(dir):
    s3_api = connect_s3()
    return s3_api.list(config(__SECTION__,'bucket'),dir)
def search_list(key,s3dir_list):
    dirname=config(__SECTION__, 'dir_dest')
    for i in s3dir_list:
        if (i['Key'] == dirname + "/" + key):
            return i
    return False
def main():
    global __SECTION__
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='configFile',default='config')
    parser.add_argument('--section', help='a section in the configfile', default='s3')
    args = parser.parse_args()
    __SECTION__=args.section
    read_config(args.config)
    format= '%(asctime)s %(message)s'
    logging.basicConfig(filename=config(args.section,'logfile'), level=logging.INFO, format=format)
    path = config(args.section, 'dir_source')
    #Load s3 list
    listdest=list_s3(config(__SECTION__, 'dir_dest') + "/")
    #list source directory
    for f in os.listdir(path):
        s=search_list(f,listdest)
        if (s != False):
            #/compare size
            size=os.stat(path +"/" + f).st_size
            if (size == s['Size']):
                print(f + " OK")
            else:
                print(f + " KO BAD SIZE" + "s3-size=" + str(s['Size']) + " /size=" + str(size))
                copy_to_s3(path +"/" + f)
                print(f + " COPIED")
        else:
            print(f + " KO NOT FOUND")
            #copy
            copy_to_s3(path +"/" + f)
            print(f + " COPIED")


if __name__ == "__main__":
    main()
