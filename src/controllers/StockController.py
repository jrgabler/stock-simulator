import mysql.connector

class StockController:

    # TODO - turn into env variable
    CONN_STRING = "host='localhost' port=3306 user='user' password=''"

    def addWatch(self, stockId: int, userId: int):
        connection = None
        try:
            connection = mysql.connector.connect(CONN_STRING)
            cursor = connection.cursor()

            cursor.execute(f"INSERT INTO WatchList(stock_id, user_id) VALUES({stockId}, {userId})")

            connection.commit()
            cursor.close()
        except mysql.DatabaseError as error:
            print(error) # TODO - log error
        finally:
            if(connection is not None):
                connection.close()

    def removeWatch(self, stockId: int):
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
