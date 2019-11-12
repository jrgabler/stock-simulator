import psycopg2 as psycopg

class StockController:

    # TODO - turn into env variable
    CONN_STRING = "host='lolcalhost' dbname='stocksimulator' user='postgres' password=''"

    def addWatch(self, stockId: int, userId: int):
        connection = None
        try:
            connection = psycopg.connect(CONN_STRING)
            cursor = connection.cursor()

            cursor.execute(f"INSERT INTO WatchList(stock_id, user_id) VALUES({stockId}, {userId})")

            connection.commit()
            cursor.close()
        except psycopg.DatabaseError as error:
            print(error) # TODO - log error
        finally:
            if(connection is not None):
                connection.close()

    def removeWatch(self, stockId: int):
        connection = None
        try:
            connection = psycopg.connect(CONN_STRING)
            cursor = connection.cursor()

            cursor.execute(f"DELETE FROM WatchList WHERE stock_id={stockId}")

            connection.commit()
            cursor.close()
        except psycopg.DatabaseError as error:
            print(error) # TODO - log error
        finally:
            if(connection is not None):
                connection.close()
