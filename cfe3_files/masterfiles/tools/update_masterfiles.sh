#!/bin/bash

SRC=$1

if [[ ! -z SRC ]]; then
  cd /var/cfengine
  aws s3 sync s3://$SRC ./ --exact-timestamps
else
  echo "Usage: ./update_masterfiles.sh S3_BUCKET"
  exit 1
fi
