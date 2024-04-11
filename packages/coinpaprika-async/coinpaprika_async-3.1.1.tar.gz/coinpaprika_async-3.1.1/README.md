<div align="center">
<h1 style="font-size:50px;">Coinpaprika Async Client</h1>

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/coinpaprika-async)

</div>

## 1. Usage

This library provides convenient and modern way to use [coinpaprika.com](https://api.coinpaprika.com/) API in Python.

[Coinpaprika](https://coinpaprika.com/) delivers full market data to the world of crypto: coin prices, volumes, market caps, ATHs, return rates and more.

## 2. Requirements

```sh
pip install coinpaprika_async
```

Or:

```sh
poetry add coinpaprika_async
```

## 3. Getting started

Each top-level path has their own endpoint class now:


- `GET` /coins `->` `CoinsEndpoint`
- `GET` /exchanges `->` `ExchangesEndpoint`
- `GET` /key `->` `KeyEndpoint`
- `GET` /global `->` `MarketEndpoint`
- `GET` /search + /price-converter `->` `MiscelanousEndpoints`
- `GET` /people `->` `PeopleEndpoint`
- `GET` /tags `->` `TagsEndpoint`
- `GET` /tickers `->` `TickersEndpoint`


## 4 Examples:

Check out the [examples](./examples) directory.

## 5. Tests

```sh
py -m pytest -vs .
```

## 6. License
CoinpaprikaAPI is available under the MIT license. See the LICENSE file for more info.
