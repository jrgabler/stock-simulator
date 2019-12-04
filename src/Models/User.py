class User:

    def __init__(self, username: str, password: str):
        self.username = username
        self.isAuthenticated = False

    def getUsername(self):
        return self.username

    def isAuthenticated(self):
        return self.isAuthenticated

    # There's no way this is the correct way to do this
    def authenticate(self):
        self.isAuthenticated = True