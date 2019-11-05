# Parent class to Stock, etc. (coming soon)
class Asset:
    def __init__(self, type: str, symbol: str):
        self.type = type
        self.symbol = symbol