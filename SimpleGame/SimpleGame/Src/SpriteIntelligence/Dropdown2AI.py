from Utils.sprites.SpriteIntelligenceBase import SpriteIntelligenceBase
class Dropdown2AI(SpriteIntelligenceBase):
    """description of class"""

    def updatePosition(self, sprite, time):
        print(sprite.moveState)
        return super().updatePosition(sprite, time)


