from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.Constants import AnimationNames

class TeleporterStyle(SpriteStyleBase):
    """Animation style of the TeleporterStyle sprite."""
    def getStyleData(self):
        result = {
            AnimationNames.Standing : {
                "Filename": "Telepunkt.png",
                "AnimationType": "TimeBased",
                "Delay": 100}
            }
        return result




