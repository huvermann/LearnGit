from Utils.SpriteItemBase import SpriteItemBase
from Utils.Constants import Direction

class SpriteItemWalkingBase(SpriteItemBase):
    """Sprite that walks back and forth."""
    def __init__(self, spritename):
        super().__init__(spritename)
        self_walkDirection = Direction.Right
        self.__animations = {}

    def configureAnimations(self, configuration):
        for ani in configuration:
            print("Animation: {0}".format(ani))
        pass

    def loadAnimationFromConfiguration(self, animationname, configuration):
        result = AnimationInfo()
        result.configure(self._spriteName, animationname, configuration)
        return result


    def update(self):
        return super().update()



