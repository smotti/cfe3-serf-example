#!/bin/bash

BUCKET=$1


print_usage() {
  echo "Usage: $0 BUCKET"
}

if [ -z $BUCKET ]; then
  echo "You must specify a AWS S3 Bucket!"
  print_usage
  exit 1
else
  for f in ./*; do
    if [ -d $f ]; then
      aws s3 sync $f s3://$BUCKET/${f:2} \
        --exclude "*.sw*" --exclude "sync_to_s3.sh" --exclude "test_*.cf" \
        --exclude "download_serf.sh" --delete
    fi
  done
fi
