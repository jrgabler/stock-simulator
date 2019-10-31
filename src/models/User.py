class User:
    # Security notes: so we should be encrypting the password on the frontend somehow
    # and it should never be visible in any way
    # Apply further encryption on the backend? Or is that overkill?
    # Is frontend encryption even possible from a client computation standpoint?
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def getUsername(self):
        return self.username