import configparser
__CONFIG__=configparser.RawConfigParser()
__SECTION__=''



def read_config(file):
    with open(file) as f:
        file_content = f.read()
    __CONFIG__.read_string(file_content)
    return __CONFIG__

def get_key(section,key,default=''):
    c=__CONFIG__[section]
    return c.get(key,default)

def get_config():
    items=__CONFIG__.items('config')
    data = {}
    for k, v in items:
        data[k] = v
    return data

def set_section(section):
    global __SECTION__
    __SECTION__=section

def get_section():
    return __SECTION__