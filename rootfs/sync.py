#!/usr/bin/python3
import sys
import os
sys.path.insert(1, os.getcwd())

import argparse

import pyinotify
import logging

from utils import config
from utils import s3_utils
from utils import sftp_utils

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
       logger=logging.getLogger();
       logger.info(f"IN_CLOSE_WRITE event detected on: {event.pathname}")
       copy_file(event.pathname)
       logger.info(f"IN_CLOSE_WRITE end of copy: {event.pathname}")
    def process_IN_DELETE(self,event):
       logger=logging.getLogger();
       logger.info(f"IN_DELETE event detected on: {event.pathname}")
       delete_file(event.pathname)
def copy_file(file):
    type=config.get_key(config.get_section(),'type','config')
    logger = logging.getLogger();
    logger.info(f"process copy_file : {type}")
    if type == 's3':
        s3_utils.copy_to_s3(file)
    elif type == 'sftp':
        sftp_utils.copy_to_sftp(file)
def delete_file(file):
    type = config.get_key(config.get_section(), 'type', 'config')
    logger = logging.getLogger();
    logger.info(f"process delete_file : {type}")
    if type == 's3':
        s3_utils.delete_to_s3(file)
    elif type == 'sftp':
        sftp_utils.delete(file)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='configFile',default='config')
    parser.add_argument('--section', help='a section in the configfile', default='config')
    args = parser.parse_args()
    config.set_section(args.section)
    config.read_config(args.config)
    format= '%(asctime)s %(message)s'
    logging.basicConfig(filename=config.get_key(args.section,'logfile'), level=logging.INFO, format=format)
    logger=logging.getLogger()
    logger.info("Start sync")
    path = config.get_key(args.section, 'dir_source')
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
