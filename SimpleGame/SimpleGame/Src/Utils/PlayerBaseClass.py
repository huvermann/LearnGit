import pygame
import os
import logging
from Utils.DirHelper import getSpriteAnimationImage
from Utils.Constants import AnimationNames

class PlayerMoveState(object):
    Standing = 1
    Falling = 2
    MoveLeft = 3
    MoveRight = 4
    JumpLeft = 5
    JumpRight = 6

class PlayerBaseClass(pygame.sprite.Sprite):
    """The player sprite base class."""
    def __init__(self, screen, spriteName):
        super().__init__()
        self.image = pygame.Surface([32,32])
        self.image.fill((0,0,0))
        self.rect = self._calculateViewPosition(screen, self.image)
        self._spriteName = spriteName
        self._aniLeft = None
        self._aniRight = None
        self._transparenceKey = None
        self.loadAnimations(spriteName)
        #Todo: replace the counter with a clock
        self._moveCounter = 0
        self._speed = 120 # Default speed pixel per second
        self._moveState = PlayerMoveState.Standing


    def _calculateViewPosition(self, screen, image):
        #Todo: 
        screeenRect = screen.get_rect()
        result = image.get_rect()
        result.left = screeenRect.centerx - result.width // 2
        result.top = screeenRect.centery - result.height // 2
        return result
        

    def loadAnimations(self, spriteName):
        """Loads all animation imanges from spritename folder."""
        self._aniLeft = PlayerBaseClass.loadAnimationFile(spriteName, AnimationNames.Left)
        self._aniRight = PlayerBaseClass.loadAnimationFile(spriteName, AnimationNames.Right)
        # Get the transparency color
        if self._aniLeft:
            self._transparenceKey = self._aniLeft.get_at((0,0))
            self._aniLeft.set_colorkey(self._transparenceKey)
        if self._aniRight:
            self._aniRight.set_colorkey(self._aniRight.get_at((0,0)))
        pass

    @property
    def moveState(self):
        return self._moveState
    @moveState.setter
    def moveState(self, value):
        self._moveState = value

    def joystickInput(self, externalInput):
        """Drives the player movestate by external device."""
        pass

    @property
    def speed(self):
        return self._speed
    

    @staticmethod
    def loadAnimationFile(spriteName, animationName):
        result = None
        animationFile = getSpriteAnimationImage(spriteName, animationName)
        if os.path.isfile(animationFile):
            result = pygame.image.load(animationFile).convert()
        return result

    def update(self):
        #todo implement state driven animation.
        logging.debug("Update player")
        pass

    def update(self, vectorX, vectorY):
        #Todo remove this method!

        # Todo: implement animation
        
        # Select the animation by x-vector
        if vectorX == -1:
            ani = self._aniLeft
        else:
            ani = self._aniRight
        
        if self._moveCounter < 10:
            rect = (0,0, 32,32)
        else:
            rect = (32,0,32,32)
        self._moveCounter +=1
        if self._moveCounter > 20:
            self._moveCounter = 0

        if ani:
            self.image = ani.subsurface(rect)




        



