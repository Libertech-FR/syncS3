#!/usr/bin/python3
import os.path
from cn_s3_api.api import CNS3Api
import argparse
import configparser
import pyinotify
import logging

__CONFIG__=configparser.RawConfigParser()
__SECTION__=''
class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
       logger=logging.getLogger();
       logger.info(f"IN_CLOSE_WRITE event detected on: {event.pathname}")
       copy_to_s3(event.pathname)
       logger.info(f"IN_CLOSE_WRITE end of copy: {event.pathname}")

    def process_IN_DELETE(self,event):
       logger=logging.getLogger();
       logger.info(f"IN_DELETE event detected on: {event.pathname}")
       delete_to_s3(event.pathname)
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
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE
    notifier = pyinotify.Notifier(wm, EventHandler())
    wm.add_watch(path, mask)
    try:
        notifier.loop()
    except KeyboardInterrupt:
        print("Stopped.")
if __name__ == "__main__":
    main()
