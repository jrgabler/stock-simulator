import mysql.connector
import datetime

from Resources import MarketProvider
from models.assets import Stock, Asset
from models import User
class AssetSell:

    # TODO - turn into env variable
    CONN_STRING = "host='localhost' port=3306 user='root' password=''"

    # Implement ability to hit purchase asset endpoints 
    @classmethod
    def purchaseAsset(cls, asset: Asset, quantity: float, userId: int):
        connection = None
        try:
            connection = mysql.connector.connect(cls.CONN_STRING)
            cursor = connection.cursor()
            #checking to see if asset type is a stock(more to be added at program grows)
            if(asset.type == "stock"):
                cursor.execute(f"SELECT last FROM Stock WHERE symbol={asset.symbol}")
                row = cursor.fetchone()
                assetPrice = row[0]
                priceAsset = assetPrice[0]
                amount = priceAsset * quantity
                cursor.execute(f"SELECT balance FROM UserTable WHERE id={userId}")
                row = cursor.fetchone()
                userBalance = row[0]
                balance = userBalance[0]
                #checks to see if user has enough $$$
                if(balance >= amount):
                    cursor.execute(f"UPDATE UserTable SET balance={balance - amount} WHERE id={userId}")
                    cursor.execute(f"SELECT id FROM Stock WHERE symbol={asset.symbol}")
                    row = cursor.fetchone()
                    stock = row[0]
                    stockID = stock[0]
                    cursor.execute(f"INSERT INTO OwnedAssetsList (stock_id,user_id,quantity,purchase_price,date_purchased,total_equity) VALUES({stockID},{userId},{quantity},{priceAsset},{datetime.datetime.now()},{amount});")
                    return "Asset purchased"
                else:
                    return "not enough money to make purches"
            else:
                return "not stock type"