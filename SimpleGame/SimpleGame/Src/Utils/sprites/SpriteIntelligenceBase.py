from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.ViewPointer import ViewPoint

class SpriteMoveState():
    FallingDown = 1
    Standing = 2
    MoveLeft = 3
    MoveRight = 4


class SpriteIntelligenceBase(object):
    """description of class"""
    def __init__(self, parentSprite, properties):
        #assert isinstance(parentSprite, SpriteBase)
        self._parentSprite = parentSprite
        self._viewPointer = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewPointer)
        self._style = self._parentSprite.style
        self.configureProperties(properties)
        pass

    def configureProperties(self, properties):
        pass



    def updatePosition(self, sprite, time):
        """Updates the position of the sprite."""
        position = self._viewPointer.mapPositionToScreenOffset(ViewPoint(sprite.x, sprite.y))
        sprite.rect.left = position.left
        sprite.rect.top = position.top
        pass






