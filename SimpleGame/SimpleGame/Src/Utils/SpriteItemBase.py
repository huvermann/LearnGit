import pygame
import os
from Utils.DirHelper import getSpriteAnimationImage
from Utils.Constants import AnimationNames
from Utils.CollosionInfo import CollosionInfo
from Utils.ViewPointer import ViewPoint
from Utils.ServiceLocator import ServiceLocator, ServiceNames
import logging

class SpriteItemBase(pygame.sprite.Sprite):
    """The sprite base class"""
    def __init__(self, spritename):
        super().__init__()
        self._spriteName = spritename
        self._viewPointer = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewPointer)
        self._position = ViewPoint(0,0)
        self.image = pygame.Surface([32,32])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.left = 20
        self.rect.top = 20
        self._rotationSpeed = 200

        self._collosionInfo = CollosionInfo(parent = self)
        self._collideCallback = self.doCollide
        pass

    def updateScreenOffset(self):
        offset = self._viewPointer.mapPositionToScreenOffset(self._position)
        self.rect.left = offset.left
        self.rect.top = offset.top
        pass

    def doCollide(self):
        """Is called when the player collides with this sprite."""
        return self._collosionInfo
    
    @staticmethod
    def getRectTimeBased(numAnimations, imageSize, millisec):
        time = pygame.time.get_ticks()
        imageNo = (time // millisec) % numAnimations
        rect = (imageSize[0] * imageNo, 0, imageSize[0], imageSize[1])
        return rect

    @staticmethod
    def countAnimationLength(animationImage):
        """Calculates the length of an animation."""
        rect = animationImage.get_rect()
        return rect.width // rect.height

    @staticmethod
    def getPictureSize(animationImage):
        rect = animationImage.get_rect()
        return (rect.height, rect.height)


    @staticmethod
    def loadAnimationFile(spriteName, animationName):
        result = None
        animationFile = getSpriteAnimationImage(spriteName, animationName)
        if os.path.isfile(animationFile):
            result = pygame.image.load(animationFile).convert()
        else:
            logging.error("Missing animation file: {0}".format(animationFile))
        return result

    def update(self):
        self.updateScreenOffset()
        pass

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        assert isinstance(value, ViewPoint), "Position type must be ViewPoint."
        self._position = value





