import pyscopg2 as psycopg

from src.models.User import Users

class UserController:

    CONN_STRING="host='localhost' dbname='stocksimulator' user='postgres' password=''"

    # Adds a new User to the database
    def add(self, user: User):
        connection = None
        try:
            connection = psycopg.connect(CONN_STRING)
            
            cursor = connection.cursor()
            cursor.execute("")
            connection.commit()
            cursor.close()
        except psycopg.DatabaseError as error:
            print(error)
        finally:
            if(connection is not None):
                connection.close()

    # Marks existing user as archived
    def archive(self, userId: int):
        # TODO - implement an archived marker on the User table
        connection = None
        try:
            connection = psycopg.connect(CONN_STRING)
            cursor = connection.cursor()

            cursor.execute("")

            connection.commit()
            cursor.close()
        except psycopg.DatabaseError as error:
            print(error)
        finally:
            if(connection is not None):
                connection.close()
