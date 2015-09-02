#!/usr/bin/env bash

# Add SSH keys to keychain
# eval $(keychain --eval --agents ssh -Q --quiet ~/.ssh/spfa-deploy-key)

# Create the emailprocessor project dir and virtualenv
mkdir -p email-processor
cd email-processor
virtualenv venv
. venv/bin/activate

rm -rf email-processor
# Use SSH for private repos for which we have a deployment key:
# git clone git@github.com:InnovativeTravel/emailprocessor.git
# For public repos simply use HTTPS
git clone https://github.com/InnovativeTravel/email-processor

# Trying to be idempotent
cd email-processor
git checkout -- .
pip install -e .
cd

# Initialize the aws credentials file
rm -rf .aws
mkdir -p .aws
touch .aws/credentials
chmod 600 .aws/credentials
