import sys
import os
sys.path.insert(1, os.getcwd())

import argparse
import logging
from utils import config
from utils import s3_utils
from utils import sftp_utils
def search_list(key,dir_list):
    dirname=config.get_key(config.get_section(), 'dir_dest')
    for i in sdir_list:
        if (i['Key'] == dirname + "/" + key):
            return i
    return False
def copy_file(file):
    type=config.get_key(config.get_section(),'type','config')
    if type == 's3':
        s3_utils.copy_to_s3(file)
    elif type == 'sftp':
        sftp_utils.copy_to_sftp(file)

def list_dest():
    dest=config.get_key(config.get_section(), 'dir_dest')
    type = config.get_key(config.get_section(), 'type',"config" )
    listdest=[]
    if type == "s3":
        listdest = s3_utils.list_s3(dest)
    elif type == "sftp":
        list=sftp_utils.list(dest)
        for f in list:
            listdest.append({'Key': f.filename,'Size': f.st_size})
    return listdest
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='configFile',default='./config.conf')
    parser.add_argument('--section', help='a section in the configfile', default='config')
    args = parser.parse_args()
    config.set_section(args.section)
    config.read_config(args.config)
    format= '%(asctime)s %(message)s'
    logging.basicConfig(filename=config.get_key(args.section,'logfile'), level=logging.INFO, format=format)
    path = config.get_key(args.section, 'dir_source')
    #Load s3 list
    listdest=list_dest()
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
                copy_file(path +"/" + f)
                print(f + " COPIED")
        else:
            print(f + " KO NOT FOUND")
            #copy
            copy_file(path +"/" + f)
            print(f + " COPIED")


if __name__ == "__main__":
    main()
