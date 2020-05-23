#!/bin/bash

apt-get update
apt-get install -y \
  docker.io \
  git

git clone https://github.com/anax32/crypto-exchanges
cd crypto-exchanges

./build-images.sh
./run-docker.sh
