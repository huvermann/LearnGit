import pygame
import os
import logging
from Utils.DirHelper import getSpriteAnimationImage, getSpriteResourceFilename
from Utils.Constants import AnimationNames, ConfigKey
from Utils.JoystickStates import JoystickEvents, JoystickState
from Utils.PlayerMoveStateMachine import PlayerMoveState, PlayerMoveStateMachine
from Utils.TileMapManager import TileMapManager
from Utils.AnimationInfo import AnimationInfo, AniConfigKeys, AnimationTypes

class PlayerBaseClass(pygame.sprite.Sprite):
    """The player sprite base class."""
    def __init__(self, screen, spriteName, position, tileMapManager):
        super().__init__()
        self._position = position
        self._tileMapManager = tileMapManager
        self.image = pygame.Surface([32,32])
        self.image.fill((0,0,0))
        self.rect = self._calculateViewPosition(screen, self.image)
        self._spriteName = spriteName
        self._mapManager = None
        self._aniLeft = None
        self._aniRight = None
        self._animations = {}
        self._transparenceKey = None
        self.loadAnimations(spriteName)
        self._speed = 120 # Default speed pixel per second
        self._fallSpeed = 200
        self._moveStateMachine = PlayerMoveStateMachine()
        self._moveStateMachine.currentPositionCallback = self.getCurrentPositionHandler
        self._moveStateMachine._getTileInfoCallback = self._getTileInfoHandler

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
        result.Filename = configuration[AniConfigKeys.Filename]
        if AniConfigKeys.MaskFilename in configuration:
            result.MaskFileName = configuration[AniConfigKeys.MaskFilename]
        if AniConfigKeys.AnimationType in configuration:
            result.AnimationType = configuration[AniConfigKeys.AnimationType]
            if result.AnimationType == AnimationTypes.TimeBased:
                result.Delay = configuration[AniConfigKeys.Delay]
            elif result.AnimationType == AnimationTypes.PositionBased:
                result.StepWith = configuration[AniConfigKeys.StepWith]
        else:
            logging.warn("No animationtype configured for animation: {0}".format(animationname))
            result.AnimationType = AnimationTypes.TimeBased
            result.Delay = 200
        #Load the files from folder
        result.ImageSurface = PlayerBaseClass.loadAnimationResourceFile(self._spriteName, result.Filename)
        if result.MaskFileName:
            result.MaskSurface = PlayerBaseClass.loadAnimationResourceFile(self._spriteName, result.MaskFileName)
        return result

    def _getTileInfoHandler(self):
        result = None
        playerPosition = (self._position.posX + self.rect.left, self._position.posY+ self.rect.top)
        result = self._tileMapManager.getTouchedTiles(playerPosition, self.rect.size)

        return result

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
    @property
    def fallSpeed(self):
        return self._fallSpeed
    
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
        if moveStateMachine.moveState in [PlayerMoveState.Standing, PlayerMoveState.MoveLeft, PlayerMoveState.MoveRight]:
            if moveStateMachine.lastChange:
                vectors = moveStateMachine.getVectors(moveStateMachine.moveState)
                duration = timeStamp - moveStateMachine.lastChange
                move = duration * self.speed / 1000 * vectors.X
                self._position.posX = int(moveStateMachine.lastPosition.posX + move)
        elif moveStateMachine.moveState in [PlayerMoveState.Falling]:
            #Falling
            if moveStateMachine.lastChange:
                duration = timeStamp - moveStateMachine.lastChange
                move = duration * self.fallSpeed / 1000
                self._position.posY = int(moveStateMachine.lastPosition.posY + move)

        pass

    def update(self):
        ticks = pygame.time.get_ticks()
        self._moveStateMachine.updateState(ticks)
        self.image = self._getImage(self.moveState, ticks)
        self._updatePosition(ticks, self._moveStateMachine)
        pass




        



