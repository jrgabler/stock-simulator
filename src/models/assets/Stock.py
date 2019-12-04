# import Asset
import json

# This object has to match the API being used in order to make json.dumps()
# work
class Stock():
    def __init__(self, open: float, close: float, high: float, low: float, average_volume: float, market_cap: float, peratio: float, dividend_yield: float, asset_type: str, last: float, symbol: str, prev_close: float):
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.average_volume = average_volume
        self.market_cap = market_cap
        self.peratio = peratio
        self.dividend_yield = dividend_yield
        self.asset_type = asset_type
        self.last = last
        self.symbol = symbol
        self.prevclose = prev_close

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        stockJson = json_str["quotes"]["quote"]
        return Stock(stockJson["open"], stockJson["close"], stockJson["high"], stockJson["low"], 0.0, 0.0, 0.0, 0.0, stockJson["type"], stockJson["last"], stockJson["symbol"], stockJson["prevclose"])
