#!/bin/bash

WGET=$(which wget)
CURL=$(which curl)
BIN_NAME=usr_local_bin_serf
DEST=./masterfiles/local_files/common
VERSION=0.8.1
URL=https://releases.hashicorp.com/serf/${VERSION}/serf_${VERSION}_linux_amd64.zip

function check_error {
  if [ $? != 0 ]; then
    echo $1
    exit 1
  fi
}

if [ ! -d $DEST ]; then
  mkdir -p $DEST
fi

if [ ! -e ${DEST}/serf_${VERSION}_linux_amd64.zip ]; then
  if [ ! -z $WGET ]; then
    wget -q -P $DEST $URL
    check_error "Failed to download serf version ${VERSION}"
  elif [ ! -z $CURL ]; then
    curl -S -s -L $URL -o ${DEST}/serf_${VERSION}_linux_amd64.zip
    check_error "Failed to download serf version ${VERSION}"
  else
    echo "Couldn't find wget nor curl!"
    exit 1
  fi

  cd $DEST
  unzip -qq serf_${VERSION}_linux_amd64.zip
  check_error "Failed to unzip serf"
  mv serf ${BIN_NAME}
  echo "Downloaded and unzipped serf to ${DEST}/${BIN_NAME}"
  exit 0
fi

if [[ -e ${DEST}/serf_${VERSION}_linux_amd64.zip && ! -e ${DEST}/${BIN_NAME} ]]; then
  cd $DEST
  unzip -qq serf_${VERSION}_linux_amd64.zip
  check_error "Failed to unzip serf"
  mv serf ${BIN_NAME}
  echo "Unzipped serf to ${DEST}/${BIN_NAME}"
  exit 0
fi
