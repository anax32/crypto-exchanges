#!/bin/sh -u

#
# exports the data from mongodb.fluentdb.test
#   removes the mongo "_id" field
#   renames the nested "time" field
#   compresses with gzip
#   writes to $OUTFILE
#

OUTFILE=dump.json.gz

docker exec \
  -it \
  mongo \
  /bin/sh -c "mongoexport -u=fluentd -p=test -d=fluentdb -c=test --quiet" \
  | jq -c '. | del(._id) | . + {"timestamp": .time[]} | del(.time)' \
  | gzip \
  > ${OUTFILE}
