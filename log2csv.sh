#!/bin/bash -u

#
# get the logs from a container,
# grep for exchange and product
# swap quote marks ('->")
# parse with jq into a csv file
# write to stdout
#

# sometimes log json is badly formatted:
#  | sed "s/'/\"/g" \

docker logs coinbase \
  | grep coinbase \
  | grep -v error \
  | grep ETH-BTC \
  | jq -r -s '.[] | [.price, .time] | @csv'
