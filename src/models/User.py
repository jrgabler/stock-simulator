class User:

    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username
        self.isAuthenticated = False

    def getUsername(self):
        return self.username

    def getUserId(self):
        return self.user_id

    def isAuthenticated(self):
        return self.isAuthenticated

    # There's no way this is the correct way to do this
    def authenticate(self):
        self.isAuthenticated = True
