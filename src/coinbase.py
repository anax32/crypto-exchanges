from time import sleep
import json
from websocket import create_connection

"""
  Coinbase Pro API
  DOCS
    https://docs.pro.coinbase.com/#websocket-feed
    https://docs.pro.coinbase.com/#the-ticker-channel
  RATE-LIMITS
  https://developers.coinbase.com/api/v2#rate-limiting
  10k requests per hour
  166 per minute (830 per 5 minute period)
  166 / 3
  ~ 50 per minute per currency

  codes are ISO4217
  https://en.wikipedia.org/wiki/ISO_4217
"""
# FIXME: check for rate-limit reset on 429 error:

class CoinbaseAPI():
  def __init__(self):
    self.name = "coinbase"
    self.uri = "wss://ws-feed.pro.coinbase.com"
    self.currencies = ["BTC-GBP", "ETH-GBP", "ETH-BTC"]

    self.conn = create_connection(self.uri)

    # create the params
    subscribe = {"type": "subscribe",
                 "channels": [{"name": "ticker",
                               "product_ids": self.currencies}]
                }
#    print(json.dumps(subscribe))

    self.conn.send(json.dumps(subscribe))

  def __call__(self):
    try:
      out = self.conn.recv()
    except ConnectionResetError:
      return {"exchange": self.name, "error": "connection reset"}

    D = json.loads(out)
    D.update({"exchange": self.name})
    return D

if __name__ == "__main__":
  api = CoinbaseAPI()

  while True:
    D = api()
    print(json.dumps(D))
    sleep(2)

