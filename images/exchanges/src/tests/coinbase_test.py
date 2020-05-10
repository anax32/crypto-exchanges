from coinbase import CoinbaseAPI

def test_coinbase_init():
  c = CoinbaseAPI()
  assert c is not None

def test_coinbase_call():
  c = CoinbaseAPI()
  D = c()
  assert D is not None

def test_coinbase_call_five_times():
  c = CoinbaseAPI()
  for _ in range(5):
    D = c()
    assert D is not None
