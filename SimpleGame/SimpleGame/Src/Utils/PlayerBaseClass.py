import pygame
import os
from Utils.DirHelper import getSpriteAnimationImage

class PlayerBaseClass(pygame.sprite.Sprite):
    """The player sprite base class."""
    def __init__(self, screen, mapPosition, spriteName):
        super().__init__()
        self.image = pygame.Surface([32,32])
        self.image.fill((0,0,0))
        self._mapPosition = mapPosition
        self.rect = self._calculateViewPosition(screen, mapPosition, self.image)
        self._spriteName = spriteName
        self._aniLeft = None
        self._aniRight = None
        self._transparenceKey = None
        self.loadAnimations(spriteName)
        #Todo: replace the counter with a clock
        self._moveCounter = 0

    def _calculateViewPosition(self, screen, mapPosition, image):
        #Todo: 
        screeenRect = screen.get_rect()
        result = image.get_rect()
        result.left = screeenRect.centerx - result.width // 2
        result.top = screeenRect.centery - result.height // 2
        return result
        

    def loadAnimations(self, spriteName):
        """Loads all animation imanges from spritename folder."""
        self._aniLeft = PlayerBaseClass.loadAnimationFile(spriteName, "Left")
        self._aniRight = PlayerBaseClass.loadAnimationFile(spriteName, "Right")
        # Get the transparency color
        if self._aniLeft:
            self._transparenceKey = self._aniLeft.get_at((0,0))
            self._aniLeft.set_colorkey(self._transparenceKey)
        if self._aniRight:
            self._aniRight.set_colorkey(self._aniRight.get_at((0,0)))
        pass

    @staticmethod
    def loadAnimationFile(spriteName, animationName):
        result = None
        animationFile = getSpriteAnimationImage(spriteName, animationName)
        if os.path.isfile(animationFile):
            result = pygame.image.load(animationFile).convert()
        return result

    def update(self, mapPosition, vectors):
        # Todo: implement animation
        if self._moveCounter < 10:
            rect = (0,0, 32,32)
        else:
            rect = (32,0,32,32)
        self._moveCounter +=1
        if self._moveCounter > 20:
            self._moveCounter = 0

        if self._aniLeft:
            self.image = self._aniRight.subsurface(rect)




        



