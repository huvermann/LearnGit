from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.Constants import AnimationNames

class MonsterBloobStyle(SpriteStyleBase):
    """Animation style of the bloob sprite."""
    def getStyleData(self):
        result = {
            AnimationNames.Standing : {
                "Filename": "MonsterBloob_green_walk_left.png",
                "AnimationType": "TimeBased",
                "Delay": 250},
            
            AnimationNames.Left : {
                "Filename": "MonsterBloob_green_walk_left.png",
                "AnimationType": "TimeBased",
                "Delay": 250},
            AnimationNames.Right : { 
                "Filename": "MonsterBloob_green_walk_right.png",
                "AnimationType": "TimeBased",
                "Delay": 250},
            AnimationNames.Falling : {
                "Filename": "MonsterBloob_green_die.png",
                "AnimationType": "TimeBased",
                "Delay": 250},
            AnimationNames.Die : {
                "Filename": "MonsterBloob_green_die.png",
                "AnimationType": "TimeBased",
                "Delay": 250}
            
            
            }
        return result




