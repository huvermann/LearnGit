from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.Constants import AnimationNames

class BloobStyleYellow(SpriteStyleBase):
    """Animation style of the bloob sprite."""
    def getStyleData(self):
        result = {
            AnimationNames.Standing : {
                "Filename": "bloob_yellow_gehen_links.png",
                "AnimationType": "TimeBased",
                "Delay": 25},
            AnimationNames.StandingLeft : {
                "Filename": "bloob_yellow_gehen_links.png",
                "AnimationType": "TimeBased",
                "Delay": 25},
            AnimationNames.StandingRight : {
                "Filename": "bloob_yellow_gehen_rechts.png",
                "AnimationType": "TimeBased",
                "Delay": 25},
            AnimationNames.Left : {
                "Filename": "bloob_yellow_gehen_links.png",
                "AnimationType": "TimeBased",
                "Delay": 25},
            AnimationNames.Right : { 
                "Filename": "bloob_yellow_gehen_rechts.png",
                "AnimationType": "TimeBased",
                "Delay": 25},
             AnimationNames.Falling : {
                "Filename": "bloob_yellow_springen.png",
                "AnimationType": "TimeBased",
                "Delay": 25}
            
            
            }
        return result


