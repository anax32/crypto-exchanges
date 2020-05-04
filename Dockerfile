from python:3-slim

add requirements.txt /tmp/requirements.txt

run pip install -r /tmp/requirements.txt

add src/coinbase.py /app/coinbase.py
add src/binance.py /app/binance.py
add src/uphold.py /app/uphold.py
add src/all.py /app/all.py

cmd python /app/all.py
# cmd python /app/binance.py
# cmd python /app/coinbase.py
# cmd python /app/uphold.py
