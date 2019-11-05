# Assets historically owned by the user
class SoldAssets(AssetMap):
    def __init__(self, asset: Asset):
        self.dictId = 1
        self.asset = {0: asset}