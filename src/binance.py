from time import sleep
import requests as R
import json
import datetime

"""
  DOCS
    https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
  SYMBOLS
    > list symbols
    curl https://api.binance.com/api/v3/exchangeInfo | jq .symbols[].symbol
  RATE-LIMITS
    unknown
    https://python-binance.readthedocs.io/en/latest/overview.html
    suggest 1200 per minute
  codes are ISO4217
  https://en.wikipedia.org/wiki/ISO_4217
"""

class BinanceAPI():
  def __init__(self):
    self.name = "binance"
    #self.uri = "https://api.binance.com/api/v1/ticker/allPrices"
    self.uri = "https://api.binance.com/api/v1/ticker/allPrices"

  def __call__(self):
    x = R.get(self.uri).json()
    T = datetime.datetime.now().isoformat()

    D = []

    for p in x:
      k = {"exchange": self.name, "time": T}
      k.update(p)
      D+=[k]

    return D

class BinanceSymbolAPI():
  def __init__(self):
    self.name = "binance"
    self.url = "https://api.binance.com/api/v3/avgPrice?symbol=%(symbol)s"
    self.symbols = [ "ETHBTC", "BATBTC", "BATETH" ]

  def __call__(self):
    out = []

    for symbol in self.symbols:
      T = datetime.datetime.now().isoformat()
      resp = R.get(self.url % {"symbol": symbol})

      if resp.status_code == 429:
        out += [{"exchange": self.name, "time": T, "symbol": symbol, "error": "rate-limit"}]
        continue
      elif resp.status_code != 200:
        out += [{"exchange": self.name, "time": T, "symbol": symbol, "error": "%i" % resp.status_code}]
        continue

      x = resp.json()
      k = {"exchange": self.name, "time": T, "symbol": symbol}
      k.update(x)
      out += [k]

    return out


if __name__ == "__main__":
  #api = BinanceAPI()
  api = BinanceSymbolAPI()

  while True:
    D = api()
    print(json.dumps(D))
    sleep(2)
