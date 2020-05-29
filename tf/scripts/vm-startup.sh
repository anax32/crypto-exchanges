#!/bin/bash

apt-get update
apt-get install -y \
  docker.io \
  git

usermod -a -G docker ubuntu

git clone --branch s3 https://github.com/anax32/crypto-exchanges
cd crypto-exchanges

./build-images.sh
./run-docker-s3.sh
