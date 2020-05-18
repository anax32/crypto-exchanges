# Crypto Exchange APIs

Captures cryptocoin exchange rates from a bunch of different exchanges.
Draws it in a ChartJS view.

## Exchanges

+ Coinbase
+ Binance
+ Poloniex
+ Uphold

### TODO

+ Kraken

# Deployments

All deployments create a docker container to log output from the exchange to
stdout, a fluentd container to capture that output and a mongodb instance for
storage and queries.

The data is tagged with the name of the exchange for query.

## Docker

`./build-images.sh ; ./run-docker.sh`

## Kubernetes

__in progress__

`./build-images.sh ; kubectl apply -f ./k8s`

# Visualisation

## ChartJS

see `web/` subdir

```bash
cd web/
python -m http.server
```
navigate to http://localhost:8080/chart.html
