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
    super(PoloniexAPI, self).__init__(
        "poloniex",
        "wss://api2.poloniex.com",
        {"command": "subscribe", "channel": 1102},
        self.parse_response
    )

    # load this bullshit currency map
    with open("poloniex-currency-ids.dat", "rb") as f:
      for x in f.readlines():
        p = x.split(",")
        self.currency_map.update({p[0]: p[1]})

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
    R = json.loads(out)

    if len(R) == 2:
      return {"exchange": self.name, "error": "subscription acknowledgement"}
    elif len(R) > 2:
      Q = R[2]
      D = {"pair-id": R[2][0],
           "last-trade-price": R[2][1],
           "lowest-ask": R[2][2],
           "highest-bid": R[2][3],
          }
      D.update({"currency": self.currency_map[R[2][0]]})
    else:
      return {"exchange": self.name, "error": "unknown response"}


if __name__ == "__main__":
  api = PoloniexAPI()

  while True:
    D = api()
    print(json.dumps(D))
    sleep(2)
