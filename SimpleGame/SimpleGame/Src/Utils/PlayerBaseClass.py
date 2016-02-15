import pygame
import os
import logging
from Utils.DirHelper import getSpriteAnimationImage, getSpriteResourceFilename
from Utils.Constants import AnimationNames, ConfigKey
from Utils.JoystickStates import JoystickEvents, JoystickState
from Utils.PlayerMoveStateMachine import PlayerMoveState, PlayerMoveStateMachine
from Utils.TileMapManager import TileMapManager
from Utils.AnimationInfo import AnimationInfo, AniConfigKeys, AnimationTypes
from Utils.JumpCalculator import JumpCalculator
from Utils.ServiceLocator import ServiceLocator, ServiceNames

class PlayerBaseClass(pygame.sprite.Sprite):
    """The player sprite base class."""
    #def __init__(self, screen, spriteName, position, tileMapManager):
    def __init__(self, spriteName):
        super().__init__()
        self._position = None #position
        self._tileMapManager = None #tileMapManager
        #self._tileMapManager2 = ServiceLocator.getGlobalServiceInstance(ServiceNames.
        self._viewPointer = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewPointer)
        self.image = pygame.Surface([32,32])
        self.image.fill((0,0,0))
        #self.rect = self._calculateViewPosition(screen, self.image)
        self.rect = pygame.Rect((0,0, 32,32))
        self._spriteName = spriteName
        #self._mapManager = None
        self._aniLeft = None
        self._aniRight = None
        self._animations = {}
        self._transparenceKey = None
        self.loadAnimations(spriteName)
        self._speed = 120 # Default speed pixel per second
        self._fallSpeed = 200
        self._jumpSpeedX = 300
        self._jumpSpeedY = 400
        self._jumpTime = 250

        self._moveStateMachine = PlayerMoveStateMachine()
        #self._moveStateMachine.currentPositionCallback = self.getCurrentPositionHandler
        self._moveStateMachine._getTileInfoCallback = self._getTileInfoHandler
        self._moveStateMachine.jumpTimeout = self._jumpTime
        g=1
        v0= 500
        vx = 100

        self._JumpCalculator = JumpCalculator(g, v0, vx)

    def configure(self, configuration):
        """Configure the player"""
        if ConfigKey.Animations in configuration:
            self.configureAnimations(configuration[ConfigKey.Animations])
        else:
            logging.warn("No player animation list found.")
        pass

    def configureAnimations(self, configuration):
        """Configure the animation from config file."""
        defaultAnimations = [AnimationNames.Standing, AnimationNames.Falling, AnimationNames.Left, AnimationNames.Right, AnimationNames.JumpLeft, AnimationNames.JumpRight, AnimationNames.JumpUp]
        for aniName in defaultAnimations:
            if aniName in configuration:
                self._animations[aniName] = self.loadAnimationFromConfiguration(aniName, configuration[aniName])
            else:
                logging.warn("Animation: {0} in player configuration.".format(aniName))
        pass

    def loadAnimationFromConfiguration(self, animationname, configuration):
        result = AnimationInfo()
        result.configure(self._spriteName, animationname, configuration)
        return result

    def _getTileInfoHandler(self):
        result = None
        #Todo implement tile info handler
        #playerPosition = (self._position.posX + self.rect.left, self._position.posY+ self.rect.top)
        #result = self._tileMapManager.getTouchedTiles(playerPosition, self.rect.size)

        return result

    #def _calculateViewPosition(self, screen, image):
    #    #Todo: 
    #    screeenRect = screen.get_rect()
    #    result = image.get_rect()
    #    result.left = screeenRect.centerx - result.width // 2
    #    result.top = screeenRect.centery - result.height // 2
    #    return result
        

    def loadAnimations(self, spriteName):
        """Loads all animation imanges from spritename folder."""
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
    @property
    def fallSpeed(self):
        return self._fallSpeed

    @property
    def jumpSpeedX(self):
        return self._jumpSpeedX
    @jumpSpeedX.setter
    def jumpSpeedX(self, value):
        self._jumpSpeedX = value

    @property
    def jumpSpeedY(self):
        return self._jumpSpeedY
    @jumpSpeedY.setter
    def jumpSpeedY(self, value):
        self._jumpSpeedY = value

    @property
    def jumpTime(self):
        return self._jumpTime
    @jumpTime.setter
    def jumpTime(self, value):
        self._jumpTime = value

    
    @staticmethod
    def loadAnimationFile(spriteName, animationName):
        result = None
        animationFile = getSpriteAnimationImage(spriteName, animationName)
        if os.path.isfile(animationFile):
            result = pygame.image.load(animationFile).convert()
        return result

    @staticmethod
    def loadAnimationResourceFile(spritename, filename):
        result = None
        resourceFile = getSpriteResourceFilename(spritename, filename)
        if os.path.isfile(resourceFile):
            result = pygame.image.load(resourceFile).convert()
        return result

    def _getAnimationByMoveState(self, moveState):
        # todo get animation by state
        result = None
        if moveState == PlayerMoveState.MoveLeft:
            result = self._animations[AnimationNames.Left]
        elif moveState == PlayerMoveState.MoveRight:
            result = self._animations[AnimationNames.Right]
        elif moveState == PlayerMoveState.JumpLeft:
            result = self._animations[AnimationNames.JumpLeft]
        elif moveState == PlayerMoveState.JumpRight:
            result = self._animations[AnimationNames.JumpRight]
        elif moveState == PlayerMoveState.Falling:
            result = self._animations[AnimationNames.Falling]
        elif moveState == PlayerMoveState.Standing:
            result = self._animations[AnimationNames.Standing]
        elif moveState == PlayerMoveState.JumpUp:
            result = self._animations[AnimationNames.JumpUp]
        else:
            result = self._animations[AnimationNames.Standing]
            logging.warn("No animation defined for movestate: {0}".format(moveState))
        return result


    def _getImage(self, moveState, time, position):
        """Get the subsurface of the animation based on moveState and time."""
        result = None
        ani = self._getAnimationByMoveState(moveState)
        self.rect.left = position.left
        self.rect.top = position.top
        if ani:
            if ani.AnimationType == AnimationTypes.TimeBased:
                index = ani.calculateTimeIndex(time)
                result = ani.getAnimationPictureByIndex(index)
            else:
                index = ani.calculatePositionIndex(position.left)
                result = ani.getAnimationPictureByIndex(index)
        return result

    #def getCurrentPositionHandler(self):
    #    """Handler to get the current position, used by the move state machine."""
    #    return self._position.copy()

    def onMoveStateJump(self, timeStamp, moveStateMachine):
        movex = 0
        movey = 0
        duration = timeStamp - moveStateMachine.lastChange
        if moveStateMachine.moveState == PlayerMoveState.JumpRight:
            #movey = duration * self.jumpSpeedY / 1000 * -1
            movey = self._JumpCalculator.calcY(duration) * -1
            movex = self._JumpCalculator.calcX(duration)
        elif moveStateMachine.moveState == PlayerMoveState.JumpLeft:
            movey = self._JumpCalculator.calcY(duration) * -1
            movex = self._JumpCalculator.calcX(duration) * -1
        elif moveStateMachine.moveState == PlayerMoveState.JumpUp:
            movey = duration * self.jumpSpeedY / 1000 * -1
        #self._position.posY = int(moveStateMachine.lastPosition.posY + movey)
        #self._position.posX = int(moveStateMachine.lastPosition.posX + movex)
        self._viewPointer.top = int(moveStateMachine.lastPosition.top + movey)
        self._viewPointer.left = int(moveStateMachine.lastPosition.left+ movex)

        pass

    def _updatePosition(self, timeStamp, moveStateMachine):
        #Todo: Implement handler for eache move state
        if moveStateMachine.moveState in [PlayerMoveState.Standing, PlayerMoveState.MoveLeft, PlayerMoveState.MoveRight]:
            if moveStateMachine.lastChange:
                vectors = moveStateMachine.getVectors(moveStateMachine.moveState)
                duration = timeStamp - moveStateMachine.lastChange
                move = duration * self.speed / 1000 * vectors.X
                #self._position.posX = int(moveStateMachine.lastPosition.posX + move)
                self._viewPointer.playerPosition.left = int(moveStateMachine.lastPosition.left + move)
        elif moveStateMachine.moveState in [PlayerMoveState.Falling]:
            #Falling
            if moveStateMachine.lastChange:
                duration = timeStamp - moveStateMachine.lastChange
                move = duration * self.fallSpeed / 1000
                #self._position.posY = int(moveStateMachine.lastPosition.posY + move)
                self._viewPointer.playerPosition.top = int(moveStateMachine.lastPosition.top + move)

        elif moveStateMachine.moveState in [PlayerMoveState.JumpLeft, PlayerMoveState.JumpRight, PlayerMoveState.JumpUp]:
            self.onMoveStateJump(timeStamp, moveStateMachine)

        pass

    def update(self):
        ticks = pygame.time.get_ticks()
        self._moveStateMachine.updateState(ticks)
        self._updatePosition(ticks, self._moveStateMachine)
        
        self.image = self._getImage(self.moveState, ticks, self._viewPointer.playerPosition)
        pass

    def configureProperties(self, properties):
        """Configure special properties."""
        pass




        



