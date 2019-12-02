import json, requests

from models.assets import Stock

class MarketProvider:

    # GLOBALS
    API_TOKEN = ""  # NEVER EVER COMMIT THIS
    API_URL = "https://sandbox.tradier.com/v1/"     # If you change the API you have to update the objects dumped to

    HEADERS = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(API_TOKEN)}

    def getStock(self, symbol: str) -> Stock:
        response = requests.get(API_URL + 'markets/quotes',
        params={'symbols': symbol, 'greeks': 'false'},
        headers={'Authorization': API_TOKEN, 'Accept': 'application/json'}

        stock = Stock()
        json.dumps(stock)
        return stock
