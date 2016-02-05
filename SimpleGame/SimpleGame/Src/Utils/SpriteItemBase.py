import pygame
import os
from Utils.DirHelper import getSpriteAnimationImage
from Utils.Constants import AnimationNames
import logging

class SpriteItemBase(pygame.sprite.Sprite):
    """The sprite base class"""
    def __init__(self, spritename, position, calcScreenPositionCallback):
        super().__init__()
        self._spriteName = spritename
        self._position = position
        self._calcScreenPositionCallback = calcScreenPositionCallback
        self.image = pygame.Surface([32,32])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.left = 20
        self.rect.top = 20
        self._rotationSpeed = 200
        self._dieOnTouch = True
        self._points = 10
        self._collideCallback = self.doCollide
        pass

    def doCollide(self):
        result = {}
        result["Die"] = self._dieOnTouch
        result["Points"] = self._points
        result["Sprite"] = self
        return result
    
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
        #Todo: select the image time based.
        pass




