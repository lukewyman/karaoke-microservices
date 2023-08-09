#!/bin/bash

export HOST_ACCESS_KEY_ID=$(aws --profile default configure get aws_access_key_id)
export HOST_AWS_SECRET_ACCESS_KEY=$(aws --profile default configure get aws_secret_access_key)

docker-compose up -d --build