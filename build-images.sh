#!/bin/bash -u

docker build \
  -t crypto.exchanges \
  -f images/exchanges/Dockerfile \
  images/exchanges/

docker build \
  -t crypto.fluent \
  -f images/fluent/Dockerfile \
  images/fluent/
