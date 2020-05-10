from websocket_subscriber import WebSocketSubscriber

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

class CoinbaseAPI(WebSocketSubscriber):
  def __init__(self):
    super(CoinbaseAPI, self).__init__(
        "coinbase",
        "wss://ws-feed.pro.coinbase.com",
        {"type": "subscribe",
                 "channels": [{"name": "ticker",
                               "product_ids": ["BTC-GBP", "ETH-GBP", "ETH-BTC"]}]
        }
    )


if __name__ == "__main__":
  from time import sleep

  api = CoinbaseAPI()

  while True:
    D = api()
    print(json.dumps(D))
    sleep(2)
