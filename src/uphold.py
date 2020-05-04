from time import sleep
import requests as R
import datetime
import json

"""
  RATE-LIMITS
  https://uphold.com/en/developer/api/documentation/#rate-limits
    are 500 per 5 minute period
    = 100 per minute / 3
    ~ 30 per minute per currency
  codes are ISO4217
  https://en.wikipedia.org/wiki/ISO_4217
"""
# FIXME: check for rate-limit reset on 429 error:
# https://uphold.com/en/developer/api/documentation/#response-headers

class UpholdAPI():
  def __init__(self):
    self.name = "uphold"
    self.url = "https://api.uphold.com/v0/ticker/%(currency)s"
    self.currencies = [ #"EUR", "GBP", "USD",
                       "BTC", "ETH"]

  def __call__(self):
    out = []

    for currency in self.currencies:
      T = datetime.datetime.now().isoformat()
      resp = R.get(self.url % {"currency": currency})

      if resp.status_code == 429:
        out += [{"exchange": self.name, "time": T, "error": "rate-limit"}]
        continue
      elif resp.status_code != 200:
        out += [{"exchange": self.name, "time": T, "error": "%i" % resp.status_code}]
        continue

      x = resp.json()

      for p in x:
        k = {"exchange": self.name, "time": T, "price": p["ask"]}
        k.update(p)
        out += [k]

    return out

if __name__ == "__main__":
  api = UpholdAPI()

  while True:
    D = api()
    print(json.dumps(D))
    sleep(2)
