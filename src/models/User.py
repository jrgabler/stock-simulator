class User:

    def __init__(self, userId: int, username: str):
        self.userId = userId
        self.username = username
        self.isAuthenticated = False

    def getUsername(self):
        return self.username

    def getUserId(self):
        return self.userId

    def isAuthenticated(self):
        return self.isAuthenticated

    # There's no way this is the correct way to do this
    def authenticate(self):
        self.isAuthenticated = True