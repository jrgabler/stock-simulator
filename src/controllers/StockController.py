# dependencies
import mysql.connector, os
from dotenv import load_dotenv
from pathlib import Path

# LOCAL
from Resources import MarketProvider
from models.assets import Stock, Asset
from models.User import User
# MYSQL CONFIG
env_path = Path('./config/') / '.env'
load_dotenv(dotenv_path=env_path)
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASS = os.getenv("MYSQL_PASSWORD")

class StockController:

    # CONN_STRING = "host='localhost' port=3306 user='root' password=''"

    # Inserts a Stock object into the Stock table and returns the generated ID
    # on success, -1 on failure
    @staticmethod
    def insertStock(stock: Stock):
        connection = None
        stockId = None
        try:
            connection = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASS, database="stocksimulator")
            cursor = connection.cursor()

            # if symbol exists in Stock table, update pricing from API
            # else, insert new
            cursor.execute(f"SELECT id FROM Stock WHERE symbol='{stock.symbol}';")
            row = cursor.fetchone()
            stockId = row[0]
            if(stockId is not None):
                # TODO - potential optimization point
                updatedStock = MarketProvider().getStock(stock.symbol)

                cursor.execute(f"UPDATE Stock SET open_price={stock.open} close_price={stock.close} high={stock.high} low={stock.low} average_volume={stock.average_volume} peratio={stock.peratio} didend_yield={stock.dividend_yield} asset_type='{stock.asset_type}' last={stock.last} symbol='{stock.symbol}' prev_close={stock.prev_close};")
                cursor.execute(f"SELECT id FROM Stock WHERE symbol='{stock.symbol}'")
                row=cursor.fetchone()
                stockId = row[0]
            else:
                # print("else statement")
                cursor.execute(f"INSERT INTO Stock VALUES({stock.open}, {stock.close}, {stock.high}, {stock.low}, {stock.average_volume}, {stock.market_cap}, {stock.peratio}, {stock.dividend_yield}, '{stock.asset_type}', {stock.last}, '{stock.symbol}', {stock.prev_close});")
                cursor.execute(f"SELECT LAST_INSERT_ID();")
                row = cursor.fetchone()
                stockId = row[0]

            connection.commit()
            cursor.close()
        except mysql.connector.Error as error:
            print(error)    # TODO
            return -1
        finally:
            if(connection is not None):
                connection.close()
            return stockId

    # Add a reference to Stock table to Watchlist associated with user_id
    @staticmethod
    def addWatch(stock: Stock, user_id: int):
        stockId = insertStock(stock)
        connection = None
        try:
            # connection = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASS, database="stocksimulator")
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="stocksimulator")
            cursor = connection.cursor()

            cursor.execute(f"INSERT INTO WatchList(stock_id, user_id) VALUES({stockId}, {user_id});")

            connection.commit()
            cursor.close()
        except mysql.connector.Error as error:
            print(error) # TODO - log error
            return {"message": "Something went wrong"}
        finally:
            if(connection is not None):
                connection.close()
            return {"message": f"Added {stock.symbol} to watchlist"}

    # Removes reference to Stock table associated with user_id from Watchlist
    @staticmethod
    def removeWatch(stockId: int, user_id: int):
        connection = None
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="stocksimulator")
            # connection = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASS, database="stocksimulator")
            cursor = connection.cursor()

            cursor.execute(f"DELETE FROM WatchList WHERE stock_id={stockId};")

            connection.commit()
            cursor.close()
        except mysql.connector.Error as error:
            print(error) # TODO - log error
        finally:
            if(connection is not None):
                connection.close()

    # @staticmethod
    # def all_stocks_watchlist(user_id: int):
    #     connection = None
    #     try:
    #         connection = mysql.connector.connect(host="localhost", user="root", password="", database="stocksimulator")
    #         # connection = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASS, database="stocksimulator")
    #         cursor = connection.cursor()
    #
    #         cursor.execute(f"SELECT stock_id FROM WatchList WHERE user_id={user_id};")
    #         row = cursor.fetchall()
    #
    #         print(row)
    #
    #         # cursor.execute("SELECT stock.open_price, stock.close_price, stock.high, stock.low, stock.average_volume," +
    #         #     "stock.market_cap, stock.peratio, stock.symbol, stock.prev_close" +
    #         #     "FROM Stock stock INNER JOIN WatchList watch ON stock.stock_id = watch.stock_id" +
    #         #     F"WHERE watch.stock_id IN ({stock_ids})")
    #
    #
    #         if(row is None):
    #             return None
    #
    #         cursor.close()
    #     except mysql.connector.Error as error:
    #         print(error) # TODO - log error
    #     finally:
    #         if(connection is not None):
    #             connection.close()
    #         return row


    @staticmethod
    def purchaseAsset(stock: Stock, user: User):
        connection = None
        try:
            # connection = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASS, database="stocksimulator")
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="stocksimulator")
            cursor = connection.cursor()
            # there's a lot to do here
            # we need to get the purchase price
            cursor.execute(f"INSERT INTO Stock VALUES({stock.open}, {stock.close}, {stock.high}, {stock.low}, {stock.average_volume}, {stock.dividend_yield}, {stock.type}, {stock.last}, '{stock.symbol}', {stock.prevclose});")
        except mysql.connector.Error as error:
            print(error) # TODO - log error
        finally:
            if(connection is not None):
                connection.close()
            return {"message": f"Purchased {stock.symbol}"}
