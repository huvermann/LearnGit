from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.ViewPointer import ViewPoint


class SpriteIntelligenceBase(object):
    """description of class"""
    def __init__(self, parentSprite):
        #assert isinstance(parentSprite, SpriteBase)
        self._parentSprite = parentSprite
        self._viewPointer = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewPointer)
        self._style = self._parentSprite.style

    def updatePosition(self, sprite, time):
        """Updates the position of the sprite."""
        position = self._viewPointer.mapPositionToScreenOffset(ViewPoint(sprite.x, sprite.y))
        sprite.rect.left = position.left
        sprite.rect.top = position.top
        pass






