class TeleporterFrontStyle(object):
    """description of class"""
from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.Constants import AnimationNames

class TeleporterFrontStyle(SpriteStyleBase):
    """Animation style of the TeleporterStyle sprite."""
    def getStyleData(self):
        result = {
            AnimationNames.Standing : {
                "Filename": "Teleporter_Front.png",
                "AnimationType": "TimeBased",
                "Delay": 100}
            }
        return result



