import json, requests, os
from models.assets.Stock import Stock
from dotenv import load_dotenv
from pathlib import Path

# load in .dotenv
env_path = Path('./config/') / '.env'
load_dotenv(dotenv_path=env_path)

class MarketProvider:

    # GLOBALS
    API_TOKEN = "4GKnvWS7XAJMIy25Mr8ZFFAGPyTZ" # os.getenv("TRADIER_API_KEY")
     # If you change the API you have to update the objects dumped to
    API_URL = "https://sandbox.tradier.com/v1"

    HEADERS = {"Authorization": "Bearer "+API_TOKEN, "Accept": "application/json"}

    @classmethod
    def getStock(cls, symbol: str):
        response = requests.get(cls.API_URL + "/markets/quotes?symbols=" + symbol,
        params={"greeks": "false"},
        headers=cls.HEADERS)

        stockJson = response.json()
        return Stock.from_json(stockJson)
