import json
import requests
from src.models.Stock import Stock

class MarketService:

    API_TOKEN = ""
    API_URL = "https://sandbox.tradier.com/v1/"

    HEADERS = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(API_TOKEN)}

    def getStock(self, symbol: str) -> Stock:
        response = requests.get(API_URL + 'markets/quotes',
        params={'symbols': symbol, 'greeks': 'false'},
        headers={'Authorization': API_TOKEN, 'Accept': 'application/json'}
        
        stock = Stock()
        json.dumps(stock)
        return stock

