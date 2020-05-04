import json
from time import sleep

from coinbase import CoinbaseAPI
from binance import BinanceSymbolAPI
from uphold import UpholdAPI

#apis = [CoinbaseAPI(), BinanceSymbolAPI(), UpholdAPI()]
apis = [CoinbaseAPI(), BinanceSymbolAPI()]

while True:
  for api in apis:
    D = api()

    if type(D) is list:
      for x in D:
        print(x)
    else:
      print(D)

    sleep (1)
