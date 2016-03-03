from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.Constants import AnimationNames

class CoinStyle(SpriteStyleBase):
    """description of class"""
    
    def __init__(self, parent):
        return super().__init__(parent)

    def getStyleData(self):
        result = {
            AnimationNames.Standing : {
                "Filename": "Coin_Ani.png",
                "AnimationType": "TimeBased",
                "Delay": 25}
            }
        return result


