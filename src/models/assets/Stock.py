# import Asset

# This object has to match the API being used in order to make json.dumps() 
# work
class Stock(Asset):
    def __init__(self, open: float, close: float, high: float, low: float, average_volume: float, market_cap: float, peratio: float, dividend_yield: float, asset_type: string, last: float, symbol: string, prev_close: float):
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
