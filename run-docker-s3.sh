#!/bin/bash -u

#
# TESTING SCRIPT
# sets up the docker images and runs
# + fluentd
# + exchange loggers
#
# -> exchange loggers write to stdout
# -> containers logdriver is fluentd container
# -> fluentd batch writes to s3 backend
#

LOG=flulog
CONF=fluentd-s3.conf
NET=netx

docker stop poloniex ; docker rm poloniex
docker stop coinbaseb ; docker rm coinbaseb
docker stop $LOG ; docker rm $LOG
docker network rm $NET

# https://docs.fluentd.org/output/s3
# https://docs.fluentd.org/how-to-guides/apache-to-s3
cat << EOF > ./config/fluentd/$CONF
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<filter s3.**>
  @type parser
  format json
  key_name log
  time_type string
  time_format %iso8601
</filter>

<match s3.**>
  @type s3

  s3_bucket ${S3_BUCKET}
  s3_region ${S3_REGION}
  path ex/logs/
  <buffer tag,time>
    @type file
    path /fluentd/log/s3
    timekey 3600 # 1 hour partition
    timekey_wait 10m
    timekey_use_utc true # use utc
    chunk_limit_size 256m
  </buffer>
</match>
EOF

docker network create $NET

docker run \
  -d -it \
  -p 24224:24224 \
  -p 24224:24224/udp \
  -v $(pwd)/fluent-data:/fluentd/log \
  -v $(pwd)/config/fluentd:/fluentd/etc \
  -e FLUENTD_CONF=$CONF \
  -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
  -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
  --name $LOG \
  --network $NET \
  crypto.fluent

docker run \
  -d -it \
  --log-driver=fluentd \
  --log-opt fluentd-address=127.0.0.1:24224 \
  --log-opt tag="docker.{{.Name}}" \
  --log-opt tag="mongo.{{.Name}}" \
  --log-opt tag="s3.{{.Name}}" \
  --name poloniex \
  --network $NET \
  crypto.exchanges \
  python src/poloniex.py

docker run \
  -d -it \
  --log-driver=fluentd \
  --log-opt fluentd-address=127.0.0.1:24224 \
  --log-opt tag="docker.{{.Name}}" \
  --log-opt tag="mongo.{{.Name}}" \
  --log-opt tag="s3.{{.Name}}" \
  --name coinbaseb \
  --network $NET \
  crypto.exchanges \
  python src/coinbase.py
