import pygame
import os
from Utils.DirHelper import getSpriteAnimationImage
from Utils.Constants import AnimationNames

class SpriteItemBase(pygame.sprite.Sprite):
    """The sprite base class"""
    def __init__(self, screen, spritename, position):
        super().__init__()
        self._screen = screen
        self._spriteName = spritename
        self._position = position
        self.image = pygame.Surface([32,32])
        self.image.fill((0,0,0))
        self.rect = self._calculatePosition(screen, self.image)
        self._rotationSpeed = 200
        pass

    def _calculatePosition(self, screen, image):
        result = image.get_rect()
        result.left = 10
        result.top = 20
        return result

    @staticmethod
    def loadAnimationFile(spriteName, animationName):
        result = None
        animationFile = getSpriteAnimationImage(spriteName, animationName)
        if os.path.isfile(animationFile):
            result = pygame.image.load(animationFile).convert()
        return result

    def update(self):
        #Todo: select the image time based.
        pass




