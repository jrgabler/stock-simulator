import json, requests

from models.assets.Stock import Stock
from models.Quote import Quote

class MarketProvider:

    # GLOBALS
    API_TOKEN = "Bearer w8KEVBlgug7OG33LSw2586sZl5gM"  # NEVER EVER COMMIT THIS
    API_URL = "https://sandbox.tradier.com/v1"     # If you change the API you have to update the objects dumped to

    HEADERS = {"Authorization": API_TOKEN, "Accept": "application/json"}

    @classmethod
    def getStock(cls, symbol: str):
        response = requests.get(cls.API_URL + "/markets/quotes?symbols=" + symbol,
        params={"greeks": "false"},
        headers=cls.HEADERS)
        
        stockJson = response.json()
        return Stock.from_json(stockJson)
