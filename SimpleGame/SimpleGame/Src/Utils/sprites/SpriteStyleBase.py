from Utils.Constants import AnimationNames
from Utils.AnimationInfo import AnimationInfo, AnimationTypes
class SpriteStyleBase(object):
    """The sprite style base class."""
    def __init__(self, parent):
        self.image = None
        self.rect = None
        self._parent = parent
        self._animations = {}
        styleData = self.getStyleData()
        self.configureAnimations(parent.assetName, styleData)
        self._currentAnimation = self.getDefaultAnimation()
        pass

    def getStyleAnimationNames(self):
        return [AnimationNames.Standing]

    def getDefaultAnimation(self):
        """Returns the default animation. Override this method the change the behavior."""
        return self._animations[AnimationNames.Standing]

    def getStyleData(self):
        """Override this method and return the style dictionary."""
        raise NotImplementedError("This is an abstract class! Please overwrite this method from your implementation class.")

    def configureAnimations(self, assetName, animationStyle):
        for aniName in animationStyle:
            self._animations[aniName] = self.loadAnimationInfo(assetName, aniName, animationStyle[aniName])
        pass

    def loadAnimationInfo(self, assetName, animationName, configData):
        result = AnimationInfo()
        result.configure(assetName, animationName, configData)
        return result

    def getImage(self, sprite, ticks):
        result = None
        if self._currentAnimation.AnimationType == AnimationTypes.TimeBased:
            index = self._currentAnimation.calculateTimeIndex(ticks)
            result = self._currentAnimation.getAnimationPictureByIndex(index)
        else:
            #Todo: defin
            index = self._currentAnimation.calculatePositionIndex(sprite.x)
            result = self._currentAnimation.getAnimationPictureByIndex(index)
        return result




    @property
    def currentAnimation(self):
        return self._currentAnimation
    @currentAnimation.setter
    def currentAnimation(self, value):
        self._currentAnimation = value

        pass






