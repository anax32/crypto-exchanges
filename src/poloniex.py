import os
import json
from time import sleep

from websocket_subscriber import WebSocketSubscriber

"""
  Poloniex API
  DOCS
    https://docs.poloniex.com/#websocket-api
    https://docs.poloniex.com/#ticker-data
  RATE-LIMITS
  https://docs.poloniex.com/#http-api
  6 calls per second
  60 per minute

  codes are given as 'currency id' lookup values
  https://docs.poloniex.com/#reference
"""
class PoloniexAPI(WebSocketSubscriber):
  def __init__(self):
    """
    channel descriptions:
      https://docs.poloniex.com/#channel-descriptions
    """
    self.channel = 1002 # ticker id

    super(PoloniexAPI, self).__init__(
        "poloniex",
        "wss://api2.poloniex.com",
        {"command": "subscribe", "channel": self.channel},
        self.parse_response
    )

    # load this bullshit currency map
    id_filename = os.environ.get("POLONIEX_DAT", "poloniex-currency-ids.dat")

    self.currency_map = {}

    with open(id_filename, "r") as f:
      for x in f.readlines():
        p = x.split(",")
        self.currency_map.update({int(p[0].strip()): p[1].strip()})

    self.conn = None
    # create the params

  def parse_response(self, response):
    """
    parse the response
    https://docs.poloniex.com/?shell#ticker-data

[ <id>, null, [ <currency pair id>, "<last trade price>", "<lowest ask>", "<highest bid>", "<percent change in last 24 hours>", "<base currency volume in last 24 hours>", "<quote currency volume in last 24 hours>", <is frozen>, "<highest trade price in last 24 hours>", "<lowest trade price in last 24 hours>" ], ... ]

For example:

[ 1002, null, [ 149, "382.98901522", "381.99755898", "379.41296309", "-0.04312950", "14969820.94951828", "38859.58435407", 0, "412.25844455", "364.56122072" ] ]
    """
    R = json.loads(response)

    if len(R) == 2 and int(R[0]) == self.channel and int(R[1]) == 1:
      return {"exchange": self.name, "info": "subscription acknowledgement for '%i'" % int(R[0])}
    elif len(R) == 1 and int(R[0]) == 1010:
      return {"exchange": self.name, "info": "heartbeat"}
    elif len(R) > 2:
      channel_id = R[0]
      sequence_id = R[1]

      if channel_id == 1002:
        # ticker
        # https://docs.poloniex.com/#ticker-data
        D = {"price": R[2][1],
             "lowest-ask": R[2][2],
             "highest-bid": R[2][3],
            }
        D.update({"currency": self.currency_map[R[2][0]]})
        return D
      else:
        # order book from currency name
        # https://docs.poloniex.com/#price-aggregated-book
        # NB: we don't do anyhting with the order-book
        mode = R[2][0][0]
        currency = R[2][0][1]["currencyPair"]

        orders = R[2][0][1]["orderBook"]
        print("orderbook len: %i" % len(orders))
        print("order 0: '%s'" % str(orders[0]))

        D = {"price": R[2][1],
             "lowest-ask": R[2][2],
             "highest-bid": R[2][3],
            }
        D.update({"currency": currency})
        return D
    else:
      return {"exchange": self.name, "error": "unknown response '%s'" % json.dumps(R)}


if __name__ == "__main__":
  api = PoloniexAPI()

  while True:
    D = api()
    print(json.dumps(D))
    sleep(2)
