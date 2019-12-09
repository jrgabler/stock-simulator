from flask import render_template
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

from controllers.StockController import StockController
from models.assets import Stock
from Resources.MarketProvider import MarketProvider

import json

parser = reqparse.RequestParser()
parser.add_argument("stock_symbol", help="", required=False)
parser.add_argument("user_id", help="", required=False)
parser.add_argument("stock_id", help="", required=False)

# Test function for MarketProvider
class GetStock(Resource):
    def post(self):
        data = parser.parse_args()
        stock = MarketProvider().getStock(data["stock_symbol"])
        
        return json.loads(stock.to_json())

# Arguments: username, stock symbol
class PurchaseAsset(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        marketProvider = MarketProvider()

        stock = marketProvider().getStock(data["stock_symbol"])
        # This is gonna be a hefty boi


class WatchAsset(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        marketProvider = MarketProvider()
        stockController = StockController()

        stock = marketProvider.getStock(data["stock_symbol"])

        return stockController.addWatch(stock, data["user_id"])

class RemoveWatchedAsset(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        stockController = StockController()

        return stockController.removeWatch(data["stock_id"], data["user_id"])
