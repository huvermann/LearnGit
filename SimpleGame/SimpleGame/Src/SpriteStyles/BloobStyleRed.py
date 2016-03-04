from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.Constants import AnimationNames

class BloobStyleRed(SpriteStyleBase):
    """Animation style of the bloob sprite."""
    def getStyleData(self):
        result = {
            AnimationNames.Standing : {
                "Filename": "bloob_red_gehen_links.png",
                "AnimationType": "TimeBased",
                "Delay": 25},
            AnimationNames.StandingLeft : {
                "Filename": "bloob_red_gehen_links.png",
                "AnimationType": "TimeBased",
                "Delay": 25},
            AnimationNames.StandingRight : {
                "Filename": "bloob_red_gehen_rechts.png",
                "AnimationType": "TimeBased",
                "Delay": 25},
            AnimationNames.Left : {
                "Filename": "bloob_red_gehen_links.png",
                "AnimationType": "TimeBased",
                "Delay": 25},
            AnimationNames.Right : { 
                "Filename": "bloob_red_gehen_rechts.png",
                "AnimationType": "TimeBased",
                "Delay": 25}
            
            
            }
        return result
