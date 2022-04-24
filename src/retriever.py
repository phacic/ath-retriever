import os
import csv
from enum import Enum
from typing import Dict, List

from loguru import logger
import requests

base_url = "https://finnhub.io/api/v1"
api_key = os.environ.get("API_KEY", "c9ijsliad3i9j7l2gkcg")


class StockSymbols(str, Enum):
    Apple = "AAPL"
    Amazon = "AMZN"
    Netflix = "NFLX"
    Facbook = "FB"
    Google = "GOOG"

    @classmethod
    def to_list(cls) -> List:
        """return symbols in a list"""
        return [el.value for el in cls]


def fetch_quote(symbol: str) -> Dict:
    """
    retrieve a quote from the api
    """

    url = f"{base_url}/quote?symbol={symbol}&token={api_key}"
    try:
        # logger.info(f"fetching quotes for {symbol}: {url}")
        res = requests.get(url=url)
        return res.json()
    except Exception as e:
        logger.exception(f"error fetching quote for {symbol}.")
        raise e


def get_quotes() -> List[Dict]:
    """
    retrieve quotes for the symbols from the api
    """
    # stores retrieved quotas
    quotes = []
    logger.info("fetching quotes...")
    for s in StockSymbols.to_list():
        data = fetch_quote(s)
        quotes.append(dict(symbol=s, quote=data))

    return quotes


def most_volatile_stock():
    """
    find the most volatile stock
    """
    quotes = get_quotes()

    # percentage points from yesterday
    percentage_points = {}

    logger.info("compting percentage points from yesterday...")
    for q in quotes:
        quote = q['quote']
        current_price = quote['c']
        prev_price = quote['pc']
        points = (abs(current_price - prev_price) / prev_price) * 100
        percentage_points[q['symbol']] = points

    mv_symbol = max(percentage_points, key=percentage_points.get)
    mv_quote = list(filter(lambda q: q['symbol'] == mv_symbol, quotes))[0]['quote']

    _data = {
        "stock_symbol": mv_symbol,
        "percentage_change": percentage_points[mv_symbol],
        "current_price": mv_quote["c"],
        "last_close_price": mv_quote["pc"],
    }

    csv_file_name = 'most_volatile_stock.csv'
    with open(csv_file_name, 'w') as csv_file:
        header = list(_data.keys())
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        writer.writerows([_data])

    logger.info(f"most volatile stock data exported to '{csv_file_name}'")


if __name__ == "__main__":

    most_volatile_stock()
