import mysql.connector, binascii, hashlib

from Models import User

class UserController:

    # TODO - turn into env variable
    CONN_STRING = "host='localhost' port=3306 user='root' password=''"

    def findByUsername(self, username: str):
        connection = None
        try:
            connection = mysql.connector.connect(CONN_STRING)
            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM UserTable WHERE username={username}")
            row = cursor.fetchone()
            if(row is None):
                return False

            cursor.close()
        except mysql.DatabaseError as error:
            print(error)
            return False
        finally:
            if(connection is not None):
                connection.close()
            return True

    # Adds a new User to the database
    def registration(self, username: str, password: str):
        connection = None
        try:
            connection = mysql.connector.connect(CONN_STRING)
            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM UserTable WHERE username={username}") # TODO
            row = cursor.fetchone()
            if(row is not None):
                return {"Error": "Unable to create new user: Duplicate username"}   # TODO

            hashedPassword, salt = hash(password)

            cursor.execute(f"INSERT INTO UserTable(username) VALUES({username})")
            cursor.execute(f"INSERT INTO LoginData(user_id, password, salt) VALUES((SELECT id WHERE username={username}), {hashedPassword}, {salt})")

            connection.commit()
            cursor.close()
        except mysql.DatabaseError as error:
            print(error)
            return {"Error": "Unable to create new user"}   # TODO
        finally:
            if(connection is not None):
                connection.close()
                return {"message": "Registration successful"}   # TODO

    # Marks existing user as archived
    def archive(self, userId: int):
        connection = None
        try:
            connection = mysql.connector.connect(CONN_STRING)
            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM UserTable WHERE id={userId}")
            row = cursor.fetchone()
            if(row is not None):
                return {"Error": "Unable to archive user: does note exist"} #TODO

            cursor.execute(f"UPDATE UserData SET archived=TRUE WHERE id={userID}")

            connection.commit()
            cursor.close()
        except mysql.DatabaseError as error:
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

    def login(self, username: str, password: str):
        connection = None
        try:
            connection = mysql.connector.connect(CONN_STRING)
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM UserTable WHERE username={username}")
            row = cursor.fetchone()
            if(row is None):
                return False

            if(validateLogin(User(username), row[0], password)):
                return True
        except mysql.DatabaseError as error:
            print(error)
            return False

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
        except mysql.DatabaseError as error:
            print(error)
            return False

    def logout(self, user: User, tokenId: str):
        connection = None
        try:
            connection = mysql.connector.connect(CONN_STRING)
            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM RevokedTokens WHERE id={tokenId}")
            row = cursor.fetchone()
            if(row is None):
                return False

            cursor.execute(f"INSERT INTO RevokedTokens(jti) VALUES({tokenId})")

            connection.commit()
            cursor.close()
        except mysql.DatabaseError as error:
            print(error)
            return False
        finally:
            if(connection is not None):
                connection.close()
            return True

    def tokenIsBlacklisted(self, jti: str):
        connection = None
        try:
            connection = mysql.connector.connect(CONN_STRING)
            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM RevokedTokens WHERE jti={jti}")
            row = cursor.fetchone()

            if(row is not None):
                return True

            cursor.close()
        except mysql.DatabaseError as error:
            print(error)
            return True
        finally:
            if(connection is not None):
                connection.close()
            return False
