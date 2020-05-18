#!/bin/bash -u

base64 -d $1 \
  | openssl \
    enc \
    -d \
    -aes-256-cbc
