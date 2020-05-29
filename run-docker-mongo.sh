#!/bin/bash -u

#
# TESTING SCRIPT
# sets up the docker images and runs
# + mongodb
# + fluentd
# + exchange loggers
#
# -> exchange loggers write to stdout
# -> containers logdriver is fluentd container
# -> fluentd forwards json data to mongodb
#

LOG=flulog
DB=mongo
CONF=fluentd-mongo.conf
NET=netx

docker stop poloniex ; docker rm poloniex
docker stop coinbaseb ; docker rm coinbaseb
docker stop $LOG ; docker rm $LOG
docker stop $DB ; docker rm $DB
docker network rm $NET

# https://docs.fluentd.org/output/mongo
# https://docs.fluentd.org/how-to-guides/apache-to-mongodb
cat << EOF > ./config/fluentd/$CONF
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<filter mongo.**>
  @type parser
  format json
  key_name log
  time_type string
  time_format %iso8601
</filter>

<match mongo.**>
  @type mongo

  connection_string mongodb://$DB:27017/fluentdb

  collection test

  user fluentd
  password test

  # interval
  <buffer>
    flush_interval 5s
  </buffer>
</match>
EOF

#<match **>
#  @type stdout
#</match>
#
#  host 127.0.0.1
#  port 27017
#  database fluentdb


cat << EOF > ./config/mongo/entrypoint.js
db.createUser({user: "fluentd", pwd: "test", roles: [{ role: "readWrite", db: "fluentdb"}]});
db.createCollection("test");
EOF

docker network create $NET

docker run \
  -d -it \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=test \
  -e MONGO_INITDB_ROOT_PASSWORD=test \
  -e MONGO_INITDB_DATABASE=fluentdb \
  -v $(pwd)/mongo-data:/data/db \
  -v $(pwd)/config/mongo:/docker-entrypoint-initdb.d/ \
  --name $DB \
  --network $NET \
  mongo

docker run \
  -d -it \
  -p 24224:24224 \
  -p 24224:24224/udp \
  -v $(pwd)/fluent-data:/fluentd/log \
  -v $(pwd)/config/fluentd:/fluentd/etc \
  -e FLUENTD_CONF=$CONF \
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
