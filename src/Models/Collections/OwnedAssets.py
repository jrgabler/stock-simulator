# Assets currently owned by the user
class OwnedAssets(AssetMap):
    def __init__(self, asset: Asset):
        self.dictId = 1
        self.asset = {0: asset}