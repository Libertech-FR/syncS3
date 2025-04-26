#!/bin/bash
if [ "$TYPE" = "sftp" ];then
  echo "generation config.conf for sftp"
  cat /template/config_sftp.conf|envsubst >/config.conf
else
  echo "generation config.conf for S3"
  cat /template/config_s3.conf|envsubst >/config.conf
fi
./sync.py --config /config.conf