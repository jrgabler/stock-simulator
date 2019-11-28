import mysql.connector

from Resources import MarketProvider

class StockController:

    # TODO - turn into env variable
    CONN_STRING = "host='localhost' port=3306 user='user' password=''"

    # Inserts a Stock object into the Stock table and returns the generated ID 
    # on success, -1 on failure
    def insertStock(self, stock: Stock):
        connection = None
        try:
            connection = mysql.connector.connect(CONN_STRING)
            cursor = connection.cursor()

            # if symbol exists in Stock table, update pricing from API
            # else, insert new
            cursor.execute(f"SELECT id FROM Stock WHERE symbol={stock.symbol}")
            row = cursor.fetchone()
            stockId = row[0]
            if(stockId is not None):
                # TODO - potential optimization point
                updatedStock = MarketProvider.getStock(stock.symbol)
                
                cursor.execute(f"UPDATE Stock SET open_price={stock.open} close_price={stock.close} high={stock.high} low={stock.low} average_volume={stock.average_volume} peratio={stock.peratio} didend_yield={stock.dividend_yield} asset_type={stock.asset_type} last={stock.last} symbol={stock.symbol} prev_close={stock.prev_close}")
                cursor.execute(f"SELECT id FROM Stock WHERE symbol={stock.symbol}")
                row=cursor.fetchone()
                stockId = row[0]
            else:
                cursor.execute(f"INSERT INTO Stock VALUES({stock.open}, {stock.close}, {stock.high}, {stock.low}, {stock.average_volume}, {stock.market_cap}, {stock.peratio}, {stock.dividend_yield}, {stock.asset_type}, {stock.last}, {stock.symbol}, {stock.prev_close})")
                cursor.execute(f"SELECT LAST_INSERT_ID()")
                row = cursor.fetchone()
                stockId = row[0]

            connection.commit()
            cursor.close()
        except mysql.DatabseError as error:
            print(error)    # TODO
            return -1
        finally:
            if(connection is not None):
                connection.close()
            return stockId

    # Add a reference to Stock table to Watchlist associated with userId
    def addWatch(self, stock: Stock, userId: int):
        stockId = insertStock(stock)
        connection = None
        try:
            connection = mysql.connector.connect(CONN_STRING)
            cursor = connection.cursor()

            cursor.execute(f"INSERT INTO WatchList(stock_id, user_id) VALUES({stockId}, {userId})")

            connection.commit()
            cursor.close()
        except mysql.DatabaseError as error:
            print(error) # TODO - log error
            return {"message": "Something went wrong"}
        finally:
            if(connection is not None):
                connection.close()
            return {"message": f"Added {stock.symbol} to watchlist"}

    # Removes reference to Stock table associated with userId from Watchlist
    def removeWatch(self, stockId: int, userId: int):
        connection = None
        try:
            connection = mysql.connector.connect(CONN_STRING)
            cursor = connection.cursor()

            cursor.execute(f"DELETE FROM WatchList WHERE stock_id={stockId}")

            connection.commit()
            cursor.close()
        except mysql.DatabaseError as error:
            print(error) # TODO - log error
        finally:
            if(connection is not None):
                connection.close()

    def purchaseAsset(self, stock: Stock, user: User):
        connection = None
        try:
            connection = mysql.connector.connect(CONN_STRING)
            cursor = connection.cursor()

            cursor.execute(f"INSERT INTO Stock VALUES({stock.open}, {stock.close}, {stock.high}, {stock.low}, {stock.average_volume}, {stock.dividend_yield}, {stock.type}, {stock.last}, {stock.symbol}, {stock.prevclose})")
            # there's a lot to do here
            # we need to get the purchase price
