from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.Constants import AnimationNames

class LifeLostMessageStyle(SpriteStyleBase):
    """This Style just shows a Message 'Life Lost'."""

    def getStyleData(self):
        result = {
            AnimationNames.Standing : {
                "Filename": "LifeLostMessage.png",
                "AnimationType": "TimeBased",
                "PictureSize" : [400,250],
                "ImageCount" : 1,
                "Delay": 100}
            }
        return result



