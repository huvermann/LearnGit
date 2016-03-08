from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.Constants import AnimationNames

class TargedpointStyle(SpriteStyleBase):
    """Animation style of the TeleporterStyle sprite."""
    def getStyleData(self):
        result = {
            AnimationNames.Standing : {
                "Filename": "Flagge5.png",
                "AnimationType": "TimeBased",
                "Delay": 100}
            }
        return result


