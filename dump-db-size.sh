#!/bin/bash -u

docker exec \
  -it mongo \
  /bin/sh -c "echo -n 'use fluentdb;\n db.test.count()' | mongo -u test -p test"
