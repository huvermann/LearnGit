from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.Constants import AnimationNames

class DrawbridgeStyle(SpriteStyleBase):
    """Animation style of the drawbridge sprite."""
    def getStyleData(self):
        result = {
            AnimationNames.Standing : {
                "Filename": "Drawbridge_Ani.png",
                "AnimationType": "TimeBased",
                "Delay": 100}
            }
        return result


