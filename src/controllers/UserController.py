# dependencies
import mysql.connector, binascii, hashlib, os
from dotenv import load_dotenv
from pathlib import Path

# LOCAL
from models import User

# MYSQL CONFIG
env_path = Path('./config/') / '.env'
load_dotenv(dotenv_path=env_path)
MYSQL_USER = os.getenv("MYSQL_USER") or "root"
MYSQL_PASS = os.getenv("MYSQL_PASSWORD") or ""

class UserController:

    # CONN_STRING = "host='localhost' port=3306 user='root' password=''"

    @staticmethod
    def findByUsername(username: str): # -> User:
        connection = None

        try:
            # connection = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASSWORD, database="stocksimulator")
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="stocksimulator")
            user = None
            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM UserTable WHERE username='{username}';")
            row = cursor.fetchone()

            if(row is None):
                return None

            user = User.User(row[0], row[1])

            cursor.close()

        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            if(connection is not None):
                connection.close()
            return user

    # Add balance to user account
    @staticmethod
    def addBalance(userId: int, amount: float):
        connection = None
        try:
            # connection = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASSWORD, database="stocksimulator")
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="stocksimulator")

            cursor = connection.cursor()

            cursor.execute(f"SELECT balance FROM UserTable WHERE id={userId};")
            row = cursor.fetchone()
            print("addBalance")
            print(row)

            newBalance = row[0] + amount
            cursor.execute(f"UPDATE UserTable SET balance={newBalance} WHERE id={userId};")
            # TODO - this could be turned into a MySQL procedure
            cursor.execute(f"INSERT INTO UserBalanceHistory (user_id, balance) VALUES({userId}, {newBalance});")

            connection.commit()
            cursor.close()
        except mysql.connector.Error as error:
            print(error)
            return {"message": "Something went wrong"}
        finally:
            if(connection is not None):
                connection.close
            return {"message": "Add balance successful"}

    # Subtract balance from user account
    @staticmethod
    def subtractBalance(userId: int, amount: float):
        connection = None
        try:
            # connection = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASSWORD, database="stocksimulator")
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="stocksimulator")

            cursor = connection.cursor()
            cursor.execute(f"SELECT balance FROM UserTable WHERE id={userId};")
            row = cursor.fetchone()
            print("subtractBalance")
            print(row)

            newBalance = row[0] - amount
            # TODO - where/how do we want to handle overdrawing?
            cursor.execute(f"UPDATE UserTable SET balance={newBalance};")
            # TODO
            cursor.execute(f"INSERT INTO UserBalanceHistory (user_id, balance) VALUES({userId}, {newBalance});")

            connection.commit()
            cursor.close()
        except mysql.connector.Error as error:
            return {"message": "Something went wrong"}
        finally:
            if(connection is not None):
                connection.close()
            return {"message": "Subtract balance successful"}

    @staticmethod
    def getUserBalanceHistory(userId):
        connection = None
        try:
            # connection = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASSWORD, database="stocksimulator")
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="stocksimulator")

            cursor = connection.cursor()

            cursor.execute(f"SELECT balance FROM UserBalanceHistory WHERE user_id={userId};")
            history = cursor.fetchall()

            cursor.close()
        except mysql.connector.Error as error:
            return {"message": "Something went wrong"}
        finally:
            if(connection is not None):
                connection.close()
            return history


    # Adds a new User to the database
    @staticmethod
    def registration(username: str, password: str): #, email: str):
        connection = None
        try:
            # connection = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASSWORD, database="stocksimulator")
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="stocksimulator")

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM UserTable WHERE username='{username}';") # TODO
                row = cursor.fetchone()
                print("registration")
                print(row)
                if(row is not None):
                    return {"Error": "Unable to create new user: Duplicate username"}   # TODO

            # hashedPassword, salt = hash(password)
                hashedPassword = "test123"
                salt = "1"

                cursor.execute(f"INSERT INTO UserTable(username) VALUES('{username}');")
                cursor.execute(f"INSERT INTO LoginData(user_id, password, salt) VALUES((SELECT id FROM UserTable WHERE username='{username}'), '{hashedPassword}', '{salt}');")

                # verify
                cursor.execute(f"SELECT * FROM UserTable WHERE username='{username}';") # TODO
                row = cursor.fetchone()
                print("registration pt2")
                print(row)

                if(row is None):
                    return {"Error": "Something went wrong, please try again."}

                connection.commit()
                cursor.close()
        except mysql.connector.Error as error:
            print(error)
            return {"message": "Unable to create new user"}   # TODO
        finally:
            if(connection is not None):
                connection.close()
            return {"message": "Registration successful"}   # TODO

    # Marks existing user as archived
    @staticmethod
    def archive(userId: int):
        connection = None
        try:
            # connection = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASSWORD, database="stocksimulator")
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="stocksimulator")

            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM UserTable WHERE id={userId};")
            row = cursor.fetchone()
            print("archive")
            print(row)

            if(row is not None):
                return {"Error": "Unable to archive user: does note exist"} #TODO

            cursor.execute(f"UPDATE UserData SET archived=TRUE WHERE id={userID};")

            connection.commit()
            cursor.close()
        except mysql.connector.Error as error:
            print(error)
            return {"Error": "Unable to archive user"}  #TODO
        finally:
            if(connection is not None):
                connection.close()
                return {"message": "User successfully archived"}    # TODO

    # secure password with sha512
    def __hash(self, password: str):
        salt = hashlib.sha512(os.urandom(60)).hexdigest().encode("ascii")
        hashedValue = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 10000)

        return (salt + binascii.hexlify(hashedValue)), salt

    @staticmethod
    def login(username: str, password: str):
        connection = None
        try:
            # connection = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASSWORD, database="stocksimulator")
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="stocksimulator")

            if connection.is_connected():
                cursor = connection.cursor()

                cursor.execute(f"SELECT * FROM UserTable WHERE username='{username}';")  ### Missing an f before query??
                row = cursor.fetchone()

                if(row is None):
                    return False

                # validate the password with salt
                cursor.execute(f"SELECT password, salt FROM LoginData WHERE user_id = {row[0]};")
                row = cursor.fetchone()
                dbPassword = row[0]
                salt = row[1]
                
                if(password == salt + dbPassword):
                    user = User.User(row[0], username)
                    user.authenticate()
                    return True

            return False
        except mysql.connector.Error as error:
            print(error)
            return False

    @staticmethod
    def logout(user: User, tokenId: str):
        connection = None
        try:
            # connection = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASSWORD, database="stocksimulator")
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="stocksimulator")

            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM RevokedTokens WHERE id={tokenId};")
            row = cursor.fetchone()
            print("logout")
            print(row)

            if(row is None):
                return False

            cursor.execute(f"INSERT INTO RevokedTokens(jti) VALUES({tokenId});")

            connection.commit()
            cursor.close()
        except mysql.connector.Error as error:
            print(error)
            return False
        finally:
            if(connection is not None):
                connection.close()
            return True

    @staticmethod
    def tokenIsBlacklisted(jti: str):
        connection = None
        try:
            # connection = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASSWORD, database="stocksimulator")
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="stocksimulator")

            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM RevokedTokens WHERE jti={jti};")
            row = cursor.fetchone()
            print("tokenIsBlacklisted")
            print(row)

            if(row is not None):
                return True

            cursor.close()
        except mysql.connector.Error as error:
            print(error)
            return True
        finally:
            if(connection is not None):
                connection.close()
            return False
