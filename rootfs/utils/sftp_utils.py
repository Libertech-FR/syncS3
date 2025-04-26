import paramiko
from utils import config
import logging
import os


def open_ssh_conn():
    """Opening a ssh client connection with parameter in ../etc/config.conf"""
    key_file=config.get_key(config.get_section(), 'private_key_file')
    try :
        pkey = paramiko.Ed25519Key.from_private_key_file(key_file)
    except Exception as e:
        # print("An exception occurred: {}".format(e))
        pass
    try:
        pkey = paramiko.RSAKey.from_private_key_file(key_file)
    except Exception as e:
        pass
    client = paramiko.SSHClient()
    policy = paramiko.AutoAddPolicy()
    client.set_missing_host_key_policy(policy)
    host = config.get_key(config.get_section(),'host')
    user = config.get_key(config.get_section(),'user')
    try:
        client.connect(host, username=user, pkey=pkey)
        return client
    except paramiko.ssh_exception.SSHException as e:
        e_dict = e.args[0]
def exec_cmd(command):
    """Exec directly a command (connexion and command)"""
    client=open_ssh_conn()
    stdin, stdout, stderr = client.exec_command(command)
    content=stdout.read().decode()
    del client, stdin, stdout, stderr
    return content
def copy_to_sftp(file):
    client = open_ssh_conn()
    sftp_client = client.open_sftp()
    filename = os.path.basename(file)
    remotefile = config.get_key(config.get_section(), 'dir_dest') + "/" + filename
    try:
        sftp_client.put(file, remotefile)
    except FileNotFoundError as err:
        logger=logging.getLogger()
        logger.error(f"File {filename} was not found on the local system")
    sftp_client.close()

def delete(file):
    client = open_ssh_conn()
    sftp_client = client.open_sftp()
    filename = os.path.basename(file)
    remotefile = config.get_key(config.get_section(), 'dir_dest') + "/" + filename
    try:
        sftp_client.remove(remotefile)
    except FileNotFoundError as err:
        logger=logging.getLogger()
        logger.error(f"File {filename} was not found on the local system")
    sftp_client.close()

def list(dir):
    client = open_ssh_conn()
    sftp_client = client.open_sftp()
    result=sftp_client.listdir_attr(dir)
    return result