class RevokedToken():

    def __init__(self, id: Int, jti: str):
        self.id = id
        self.jti = jti
        self.isBlacklisted = True

    def isBlacklisted(self, jti: str):
        return self.isBlacklisted