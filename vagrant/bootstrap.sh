#!/usr/bin/env bash

# Add SSH keys to keychain
# eval $(keychain --eval --agents ssh -Q --quiet ~/.ssh/spfa-deploy-key)

# Create the emailprocessor project dir and virtualenv
mkdir -p emailprocessor
cd emailprocessor
virtualenv venv
rm -rf emailprocessor
git clone git@github.com:InnovativeTravel/emailprocessor.git
. venv/bin/activate
cd emailprocessor

# Trying to be idempotent
git checkout -- .
pip install -e .
cd

# Initialize the aws credentials file
rm -rf .aws
mkdir -p .aws
touch .aws/credentials
chmod 600 .aws/credentials
