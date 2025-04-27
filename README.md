# syncS3
sync a local folder to S3. 

## Description 
SyncS3 is a little utlity that watch file changes in a directory and push them via S3 or sftp
it uses notification of the kernel to see what files are wrote (works only on linux)

## How to use it 
All is ready in a docker image. You have just to set some parameters 

### docker-compose.yml 
```
services: 
 app:
    env_file: .env
    build: .
    container_name: "sync"
    volumes:
      - ./data/storage:/data
      - ./logs:/var/log/s3sync
```
the directory to watch must mounted in volume. In this exemple (for bareos : /home/docker/bareos-sd/data/storage)

### variables for S3
file .env
```
## Endpoint S3 
S3_ENDPOINT=https://s3.rbx.io.cloud.ovh.net/
## Key Id
S3_KEY_ID=xx
## Secret
S3_KEY_SECRET=xx
## Region
S3_REGION=RBX
## bucket
S3_BUCKET=My-Bucket
## dir_source (always /data) mounted volume
S3_DIR_SOURCE=/data 
## Prefix S3 exemple file foo.txt will be named /data-sd1/foo.txt in S3
S3_DIR_DEST=/data-sd1 
```

### variables for sftp
file .env
```
TYPE="sftp"
SFTP_HOST="mysftp.server.com"
SFTP_USER="myuser"
DIR_SOURCE="/data"
DIR_DEST="/home/myuser/test"
SFTP_PRIVATE_KEY_FILE="/conf/id_ed25519"
```
