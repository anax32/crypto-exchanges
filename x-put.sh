#!/bin/bash -u

openssl \
  enc \
  -aes-256-cbc \
  -in $1 \
  | base64
