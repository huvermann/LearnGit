import pygame
import os
import logging
from Utils.DirHelper import getSpriteAnimationImage
from Utils.Constants import AnimationNames
from Utils.JoystickStates import JoystickEvents, JoystickState
from Utils.PlayerMoveStateMachine import PlayerMoveState, PlayerMoveStateMachine


class PlayerBaseClass(pygame.sprite.Sprite):
    """The player sprite base class."""
    def __init__(self, screen, spriteName, position):
        super().__init__()
        self._position = position
        self.image = pygame.Surface([32,32])
        self.image.fill((0,0,0))
        self.rect = self._calculateViewPosition(screen, self.image)
        self._spriteName = spriteName
        self._aniLeft = None
        self._aniRight = None
        self._transparenceKey = None
        self.loadAnimations(spriteName)
        self._speed = 120 # Default speed pixel per second
        self._moveStateMachine = PlayerMoveStateMachine()
        self._moveStateMachine.currentPositionCallback = self.getCurrentPositionHandler



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
        return self._moveStateMachine.moveState
    @moveState.setter
    def moveState(self, value):
        self._moveStateMachine.moveState = value

    def joystickChanged(self, externalInput):
        """Drives the player movestate by external device."""
        #self._joystickState.joystickChanged(externalInput)
        self._moveStateMachine.joystickChanged(externalInput)
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

    def _getImage(self, moveState, time):
        #Todo: Calculate rect by time or x position
        rect = (0,0, 32,32)
        if moveState == PlayerMoveState.MoveLeft:
            ani = self._aniLeft
        else:
            ani = self._aniRight
        result = ani.subsurface(rect)
        return result

    def getCurrentPositionHandler(self):
        """Handler to get the current position, used by the move state machine."""
        return self._position.copy()

    def _updatePosition(self, timeStamp, moveStateMachine):
        if moveStateMachine.lastChange:
            vectors = moveStateMachine.getVectors(moveStateMachine.moveState)
            duration = timeStamp - moveStateMachine.lastChange
            move = duration * self.speed / 1000 * vectors.X
            self._position.posX = int(moveStateMachine.lastPosition.posX + move)
        pass

    def update(self):
        #todo implement state driven animation.
        #self._position.posX += 2
        ticks = pygame.time.get_ticks()
        self._moveStateMachine.updateState(ticks)
        self.image = self._getImage(self.moveState, ticks)
        self._updatePosition(ticks, self._moveStateMachine)
        pass

    #def update(self, vectorX, vectorY):
    #    #Todo remove this method!

    #    # Todo: implement animation
        
    #    # Select the animation by x-vector
    #    if vectorX == -1:
    #        ani = self._aniLeft
    #    else:
    #        ani = self._aniRight
        
    #    if self._moveCounter < 10:
    #        rect = (0,0, 32,32)
    #    else:
    #        rect = (32,0,32,32)
    #    self._moveCounter +=1
    #    if self._moveCounter > 20:
    #        self._moveCounter = 0

    #    if ani:
    #        self.image = ani.subsurface(rect)




        



