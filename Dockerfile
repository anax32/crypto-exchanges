from python:3-slim

add requirements.txt /tmp/requirements.txt

run pip install -r /tmp/requirements.txt

workdir /app
add src /app/src

env POLONIEX_DAT=/app/src/poloniex-currency-ids.dat

run nosetests -v

cmd python /app/src/all.py
# cmd python /app/binance.py
# cmd python /app/coinbase.py
# cmd python /app/uphold.py
