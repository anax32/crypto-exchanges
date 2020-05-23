#!/bin/sh -u

OUTFILE=dump.json.gz

docker exec \
  -it \
  mongo \
  /bin/sh -c "mongoexport -u=fluentd -p=test -d=fluentdb -c=test --quiet" \
  | gzip \
  > ${OUTFILE}
