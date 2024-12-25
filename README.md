# syncS3
sync a local folder to S3. 

## Description 
SyncS3 is a little utlity that watch file changes in a directory and push them in a S3 
it uses notification of the kernel to see what files are wrote 

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
      - /home/docker/bareos-sd/data/storage:/data
      - ./logs:/var/log/s3sync
```
the directory to watch must mounted in volume. In this exemple (for bareos : /home/docker/bareos-sd/data/storage)

### variables 
fichier .env
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
DIR_SOURCE=/data 
## Prefix S3 exemple file foo.txt will be named /data-sd1/foo.txt in S3
S3_DIR_DEST=/data-sd1 
```

