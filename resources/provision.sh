#!/bin/bash -xe
# General provisioning script for vagrant boxes.
# NOTE: You have to provide ACCESS_KEY_ID and SECRET_ACCESS_KEY !!
#       And DON'T just write them into this script!! ^^

export DEBIAN_FRONTEND=noninteractive
INSTALL='apt-get install --no-install-recommends -y'

# AWS CLI tool is used by cfengine to sync masterfiles from AWS S3
$INSTALL awscli

# AWS CLI configuration
if [[ ! -d /root/.aws ]]; then
  mkdir /root/.aws
fi

cat > /root/.aws/config <<EOF
[default]
region=ap-northeast-1
output=json
EOF

cat > /root/.aws/credentials <<EOF
[default]
aws_access_key_id=$ACCESS_KEY_ID
aws_secret_access_key=$SECRET_ACCESS_KEY
EOF

# Install jq, because it is used by CFE3 promises
$INSTALL jq

# CFEngine
$INSTALL apt-transport-https
wget -qO - https://cfengine-package-repos.s3.amazonaws.com/pub/gpg.key | apt-key add -
echo "deb https://cfengine-package-repos.s3.amazonaws.com/pub/apt/packages stable main" > \
  /etc/apt/sources.list.d/cfengine-community.list
if [[ -z $(dpkg -l | grep cfengine-community) ]]; then
  apt-get update
  $INSTALL cfengine-community=3.7.4-1
fi

# Bootstrap
if [[ ! -e /var/cfengine/inputs/update.cf ]]; then
  IP=$(ip -4 -o addr show dev eth1 primary | awk '{print $4}' | cut -d / -f 1)
  cf-agent -B $IP
fi

# Copy CFE3 files from host
cp -R /vagrant/cfe3_files/* /var/cfengine/.

# Update masterfiles
#cf-agent -KI -D DEBUG -f update.cf

# Provision box
cf-agent -KI -D DEBUG
