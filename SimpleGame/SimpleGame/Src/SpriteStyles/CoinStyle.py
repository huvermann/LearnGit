from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.Constants import AnimationNames

class CoinStyle(SpriteStyleBase):
    """Animation style of the coin sprite."""
    
    #def __init__(self, parent):
    #    return super().__init__(parent)

    def getStyleData(self):
        result = {
            AnimationNames.Standing : {
                "Filename": "Coin_Ani.png",
                "AnimationType": "TimeBased",
                "Delay": 15}
            }
        return result


