import os

from poloniex import PoloniexAPI

def test_poloniex_init():
  c = PoloniexAPI()
  assert c is not None

def test_poloniex_dat_file_in_env():
  assert "POLONIEX_DAT" in os.environ

def test_poloniex_currency_map_is_not_none():
  c = PoloniexAPI()
  assert c.currency_map is not None

def test_poloniex_currency_map_is_not_empty():
  c = PoloniexAPI()
  assert len(c.currency_map) > 0

def test_poloniex_call():
  c = PoloniexAPI()
  D = c()
  assert D is not None
