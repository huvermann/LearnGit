from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.Constants import AnimationNames

class HeartStyle(SpriteStyleBase):
    """Animation style of the heard sprite."""
    def getStyleData(self):
        result = {
            AnimationNames.Standing : {
                "Filename": "Heart_Ani.png",
                "AnimationType": "TimeBased",
                "Delay": 100}
            }
        return result


