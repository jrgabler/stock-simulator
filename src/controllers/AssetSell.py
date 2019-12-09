import mysql.connector

from Resources import MarketProvider
from models.assets import Stock, Asset
from models import User
class AssetSell:

    # TODO - turn into env variable
    CONN_STRING = "host='localhost' port=3306 user='root' password=''"

    # Implement ability to sett assets 
    # on success, -1 on failure
    @classmethod
    def sellAsset(cls, asset: Asset, quantity: float, userId: int):
        connection = None
        try:
            connection = mysql.connector.connect(cls.CONN_STRING)
            cursor = connection.cursor()

            # checks to see if symbol exists in asset table 
            cursor.execute(f"SELECT OwnedAssetsList.id FROM OwnedAssetsList WHERE OwnedAssetsList.user_id ={userId} AND OwnedAssetsList.stock_id in (SELECT Stock.id FROM Stock WHERE Stock.symbol={asset.symbol})")
            row = cursor.fetchone()
            ownedAsset = row[0]
            cursor.execute(f"SELECT OwnedAssetsList.quantity FROM OwnedAssetsList WHERE OwnedAssetsList.user_id ={userId} AND OwnedAssetsList.stock_id in (SELECT Stock.id FROM Stock WHERE Stock.symbol={asset.symbol})")
            row = cursor.fetchone()
            quantityAsset = row[0]
            if(ownedAsset is not None):
                #checks if the quantity the user is trying to sell is higher than user owns
                if(quantity > quantityAsset[0]):
                    #checking to see if asset type is a stock(more to be added at program grows)
                    if(asset.type == "stock"):
                        cursor.execute(f"SELECT last FROM Stock WHERE symbol={asset.symbol}")
                        row = cursor.fetchone()
                        assetPrice = row[0]
                        priceAsset = assetPrice[0]
                        anount = priceAsset * quantity
                        cursor.execute(f"SELECT balance FROM UserTable WHERE id={userId}")
                        row = cursor.fetchone()
                        userBalance = row[0]
                        balance = userBalance[0]
                        cursor.execute(f"UPDATE UserTable SET balance={balance + amount} WHERE id={userId}")
                        cursor.execute(f"DELETE FROM OwnedAssetsList WHERE OwnedAssetsList.user_id ={userId} AND OwnedAssetsList.stock_id in (SELECT Stock.id FROM Stock WHERE Stock.symbol={asset.symbol})")
                        return "Asset sold"
                    else:
                        return "not stock type"
                else:
                    return "Do not own that many assets"
            else:
                return "Do not own asset"
            connection.commit()
            cursor.close()
        except mysql.DatabseError as error:
            print(error)    # TODO
            return -1
