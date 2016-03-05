from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.Constants import AnimationNames

class BlobNames(object):
    Left = "links_und_mitte"
    Right = "rechts_und_mitte"
    Die = "sterben"
    Jump = "springen"

class BloobStyle(SpriteStyleBase):
    """Animation style of the bloob sprite."""
    def getStyleData(self):
        result = {
            AnimationNames.Standing : {
                "Filename": "bloob_gehen_links.png",
                "AnimationType": "TimeBased",
                "Delay": 25},
            AnimationNames.StandingLeft : {
                "Filename": "bloob_gehen_links.png",
                "AnimationType": "TimeBased",
                "Delay": 25},
            AnimationNames.StandingRight : {
                "Filename": "bloob_gehen_rechts.png",
                "AnimationType": "TimeBased",
                "Delay": 25},
            AnimationNames.Left : {
                "Filename": "bloob_gehen_links.png",
                "AnimationType": "TimeBased",
                "Delay": 25},
            AnimationNames.Right : { 
                "Filename": "bloob_gehen_rechts.png",
                "AnimationType": "TimeBased",
                "Delay": 25},
            AnimationNames.Falling : {
                "Filename": "Bloob_springen.png",
                "AnimationType": "TimeBased",
                "Delay": 25}
            
            
            }
        return result




