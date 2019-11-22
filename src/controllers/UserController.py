import mysql.connector, binascii, hashlib

from src.models.User import Users

class UserController:

    # TODO - turn into env variable
    CONN_STRING = "host='localhost' port=3306 user='user' password=''"

    # Adds a new User to the database
    def add(self, userName: str, password: str):
        connection = None
        try:
            connection = mysql.connector.connect(CONN_STRING)
            cursor = connection.cursor()

            hashedPassword, salt = hash(password)

            cursor.execute(f"INSERT INTO UserTable(username) VALUES({userName})")
            cursor.execute(f"INSERT INTO LoginData(user_id, password, salt) VALUES((SELECT id WHERE username={userName}), {hashedPassword}, {salt})")
            
            connection.commit()
            cursor.close()
        except mysql.DatabaseError as error:
            print(error)
        finally:
            if(connection is not None):
                connection.close()

    # Marks existing user as archived
    def archive(self, userId: int):
        connection = None
        try:
            connection = mysql.connector.connect(CONN_STRING)
            cursor = connection.cursor()

            cursor.execute(f"UPDATE UserData SET archived=TRUE WHERE id={userID}")

            connection.commit()
            cursor.close()
        except mysql.DatabaseError as error:
            print(error)
        finally:
            if(connection is not None):
                connection.close()

    # secure password with sha512
    def __hash(self, password: str):
        salt = hashlib.sha512(os.urandom(60)).hexdigest().encode("ascii")
        hashedValue = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 10000)

        return (salt + binascii.hexlify(hashedValue)), salt

    def validateLogin(self, user: User, userId: str, password: str):
        connection = None
        try:
            connection = mysql.connector.connect(CONN_STRING)
            cursor = connection.cursor()

            # get the salt and password
            cursor.execute("SELECT password, salt FROM LoginData WHERE user_id = {userId}")
            row = cursor.fetchone()

            dbPassword = row[0]
            salt = row[1]

            if(password == salt + dbPassword):
                user.authenticate()
                return True

            return False
