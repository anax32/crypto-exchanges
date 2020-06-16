import os
import json
from time import time, sleep

from websocket_subscriber import WebSocketSubscriber

"""
  Coinjar API
  DOCS
    https://docs.exchange.coinjar.com/trading-api/#/reference/products/product-collection/list-all-products
    https://docs.exchange.coinjar.com/data-api/
    https://docs.exchange.coinjar.com/data-feed/
  RATE-LIMITS
    UNKNOWN
"""
class CoinjarAPI(WebSocketSubscriber):
  def __init__(self):
    """
    channel descriptions:
      https://docs.poloniex.com/#channel-descriptions
    """
    super(CoinjarAPI, self).__init__(
        "coinjar",
        "wss://feed.exchange.coinjar.com/socket/websocket",
        {"topic": "ticker:BTCETH", "event": "phx_join", "payload": {}, "ref": 0 },
        self.parse_response
    )

    self.heartbeat_min_interval = 42
    self.heartbeat = time()


  def parse_response(self, response):
    """
    use the parse response callback to send a heartbeat every 45s
    """
    if time() - self.heartbeat < self.heartbeat_min_interval:
      self.conn.send(json.dumps({"topic": "phoenix", "event": "heartbeat", "payload": {}, "ref": 0 }))

    return super(CoinJarAPI, self).default_parse_fn(response)

if __name__ == "__main__":
  api = PoloniexAPI()

  while True:
    D = api()
    print(json.dumps(D))
    sleep(2)
