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
#from Tiled.TiledWatcher import CheckDirection

class PlayerBaseClass(pygame.sprite.Sprite):
    """The player sprite base class."""
    #def __init__(self, screen, spriteName, position, tileMapManager):
    def __init__(self, spriteName):
        super().__init__()
        self._viewPointer = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewPointer)
        self.image = pygame.Surface([32,32])
        self.image.fill((0,0,0))
        #self.rect = self._calculateViewPosition(screen, self.image)
        self.rect = pygame.Rect((0,0, 32,32))
        self._spriteName = spriteName
        self._animations = {}
        self._transparenceKey = None
        self.loadAnimations(spriteName)

        self._JumpCalculator = JumpCalculator(jumpUpSpeed = 200, jumpUpTime = 500)
        #self._JumpCalculator.jumpUpSpeed = 200
        #self._JumpCalculator.jumpUpTime = 500

        self._moveStateMachine = PlayerMoveStateMachine(self)


    def configure(self, configuration):
        """Configure the player"""
        if ConfigKey.Animations in configuration:
            self.configureAnimations(configuration[ConfigKey.Animations])
        else:
            logging.warn("No player animation list found.")
        pass

    def configureAnimations(self, configuration):
        """Configure the animation from config file."""
        defaultAnimations = [AnimationNames.Standing, AnimationNames.StandingLeft, AnimationNames.StandingRight, AnimationNames.Falling, 
                             AnimationNames.Left, AnimationNames.Right, AnimationNames.JumpLeft, 
                             AnimationNames.JumpRight, AnimationNames.JumpUp, AnimationNames.FallingLeft, AnimationNames.FallingRight]
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
        elif moveState == PlayerMoveState.FallingLeft:
            result = self._animations[AnimationNames.FallingLeft]
        elif moveState == PlayerMoveState.FallingRight:
            result = self._animations[AnimationNames.FallingRight]

        elif moveState == PlayerMoveState.Standing:
            result = self._animations[AnimationNames.Standing]
        elif moveState == PlayerMoveState.StandingLeft:
            result = self._animations[AnimationNames.StandingLeft]
        elif moveState == PlayerMoveState.StandingRight:
            result = self._animations[AnimationNames.StandingRight]
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



    def onMoveStateJump(self, timeStamp, moveStateMachine):
        if self._moveStateMachine._MoveEndFlag:
            # Move has ended
            pass
        else:
            movex = 0
            movey = 0
            duration = timeStamp - moveStateMachine.lastChange
            if moveStateMachine.moveState == PlayerMoveState.JumpRight:
                movey = self._JumpCalculator.calcY(duration) * -1
                movex = self._JumpCalculator.calcX(duration)
            elif moveStateMachine.moveState == PlayerMoveState.JumpLeft:
                movey = self._JumpCalculator.calcY(duration) * -1
                movex = self._JumpCalculator.calcX(duration) * -1
            elif moveStateMachine.moveState == PlayerMoveState.JumpUp:
                #movey = duration * self.jumpSpeedY / 1000 * -1
                movey = self._JumpCalculator.calcJumpUp(duration)

            self._viewPointer.playerPositionX = int(moveStateMachine.lastPosition.left+ movex)
            self._viewPointer.playerPositionY = int(moveStateMachine.lastPosition.top + movey)

        pass

    def _fixGroundingPosition(self, moveStateMachine):
        info = moveStateMachine.collider.currentState
        if not info.isDockGround:
                self._viewPointer.playerPositionY -= 1

    def fixWallCollide(self, moveStateMachine):
        
        info = moveStateMachine.collider.currentState
        if info.isLeftTouched:
            self._viewPointer.playerPositionX += 4
        elif info.isRightToched:
            self._viewPointer.playerPositionX -= 4

        pass


    def _updatePosition(self, timeStamp, moveStateMachine):
        #Todo: Implement handler for eache move state
        if moveStateMachine.moveState in [PlayerMoveState.MoveLeft, PlayerMoveState.MoveRight]:
            if moveStateMachine.lastChange:
                if moveStateMachine._MoveEndFlag:
                    # Move has ended. 
                    self._viewPointer.playerPositionX = moveStateMachine._MoveEndFlag[1].left
                    self._viewPointer.playerPositionY = moveStateMachine._MoveEndFlag[1].top
                    moveStateMachine._MoveEndFlag = None
                    pass

                vectors = moveStateMachine.getVectors(moveStateMachine.moveState)
                duration = timeStamp - moveStateMachine.lastChange
                move = self._JumpCalculator.calcWalking(duration, vectors.X)
                self._viewPointer.playerPositionX = int(moveStateMachine.lastPosition.left + move)

        elif moveStateMachine.moveState in [PlayerMoveState.Falling, PlayerMoveState.FallingLeft, PlayerMoveState.FallingRight]:
            #Falling
            if moveStateMachine.lastChange:
                duration = timeStamp - moveStateMachine.lastChange
                move = self._JumpCalculator.calcFalling(duration)
                self._viewPointer.playerPositionY =  int(moveStateMachine.lastPosition.top + move)
        elif moveStateMachine.moveState in [PlayerMoveState.Standing, PlayerMoveState.StandingLeft, PlayerMoveState.StandingRight]:
            if self._moveStateMachine._MoveEndFlag:
                self._viewPointer.playerPositionX = moveStateMachine._MoveEndFlag[1].left
                self._viewPointer.playerPositionY = moveStateMachine._MoveEndFlag[1].top
                self._moveStateMachine._MoveEndFlag = None

            moveStateMachine.collider.setPlayerPosition(self._viewPointer.getPlayerMapPosition())
            self._fixGroundingPosition(moveStateMachine)
            self.fixWallCollide(moveStateMachine)

        elif moveStateMachine.moveState in [PlayerMoveState.JumpLeft, PlayerMoveState.JumpRight, PlayerMoveState.JumpUp]:
            self.onMoveStateJump(timeStamp, moveStateMachine)

        pass

    def update(self):
        ticks = pygame.time.get_ticks()
        self._moveStateMachine.updateState(ticks)
        self._updatePosition(ticks, self._moveStateMachine)
        
        self.image = self._getImage(self.moveState, ticks, self._viewPointer.playerOffset)
        pass

    def configureProperties(self, properties):
        """Configure special properties."""
        pass

    @property
    def speed(self):
        return self._speed
    @property
    def fallSpeed(self):
        return self._fallSpeed

    @property
    def jumpTime(self):
        return self._moveStateMachine.jumpTimeout
    @jumpTime.setter
    def jumpTime(self, value):
        self._moveStateMachine.jumpTimeoute = value

    @property
    def jumpG(self):
        return self._JumpCalculator.g
    @jumpG.setter
    def jumpG(self, value):
        self._JumpCalculator.g = value

    @property
    def jumpV0(self):
        return self._JumpCalculator.v0
    @jumpV0.setter
    def jumpV0(self, value):
        self._JumpCalculator.v0 = value

    @property
    def jumpVx(self):
        return self._JumpCalculator.vx
    @jumpVx.setter
    def jumpVx(self, value):
        self._JumpCalculator.vx = value

    @property
    def collideRect(self):
        """Returns the rectangel that causes a collisoin with the background."""
        return self.rect

    @property
    def collider(self):
        return self._moveStateMachine.collider

    @property
    def jumpCalculator(self):
        return self._JumpCalculator





        



