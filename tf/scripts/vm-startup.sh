#!/bin/bash

apt-get update
apt-get install -y \
  docker.io \
  git

git clone --branch s3 https://github.com/anax32/crypto-exchanges
cd crypto-exchanges

./build-images.sh
AWS_REGION=eu-west-2 ./run-docker-s3.sh
