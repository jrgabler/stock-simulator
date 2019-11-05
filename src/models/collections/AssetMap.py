from src.models.assets.Asset import Asset

class AssetMap:
    def __init__(self, asset: Asset):
        self.dictId = 1
        self.asset = {0: asset}

    # Adds Asset to dictionary with unique incremental id
    def add(asset: Asset):
        self.asset[self.dictId: asset]
        self.dictId = self.dictId + 1

    # Attempts to drop key-value pair from dictionary
    # Throws KeyError if key not found
    def remove(dictId: int):
        try:
            self.asset.pop(dictId)
        except KeyError:
            print(f"Key {dictId} not found")