import pygame
from Utils.Constants import AnimationNames, ConfigKey
from Utils.AnimationInfo import AnimationInfo, AniConfigKeys, AnimationTypes
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.JumpCalculator import JumpCalculator
from Utils.player.MoveStateMachine import MoveStateMachine
from Utils.player.PlayerMoveState import PlayerMoveState
from Utils.player.PlayerPositionUpdater import PlayerPositionUpdater



class PlayerBase(pygame.sprite.Sprite):
    """The Player base class."""
    def __init__(self, spriteName):
        super().__init__()
        self.image = pygame.Surface([2,2])
        self.image.fill((0,0,0))
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.rect = self.image.get_rect()
        self._spriteName = spriteName
        self._animations = {}
        self._stateToAnimationMapper = None
        self._moveCalculator = JumpCalculator(jumpUpSpeed = 0.2, jumpUpTime = 500)
        self._moveStateMachine = MoveStateMachine(self)
        self._viewPointer = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewPointer)
        self._positionUpdater = PlayerPositionUpdater(self, self._viewPointer)
        self._collideRect = self.rect
        self._moveStartTime = None
        self._moveStartPosition = None
        
         
    def animationList(self):
        result = [AnimationNames.Standing, AnimationNames.StandingLeft, AnimationNames.StandingRight, AnimationNames.Falling, 
                             AnimationNames.Left, AnimationNames.Right, AnimationNames.JumpLeft, 
                             AnimationNames.JumpRight, AnimationNames.JumpUp, AnimationNames.FallingLeft, AnimationNames.FallingRight, AnimationNames.Climb]
        return result

    def getAnimationMapping(self):
        result = {}
        result[PlayerMoveState.MoveLeft] = self._animations[AnimationNames.Left]
        result[PlayerMoveState.MoveRight] = self._animations[AnimationNames.Right]
        result[PlayerMoveState.ClimbUp] = self._animations[AnimationNames.Climb]
        result[PlayerMoveState.ClimbDown] = self._animations[AnimationNames.Climb]
        result[PlayerMoveState.Falling] = self._animations[AnimationNames.Falling]
        result[PlayerMoveState.FallingRight] = self._animations[AnimationNames.FallingRight]
        result[PlayerMoveState.JumpLeft] = self._animations[AnimationNames.JumpLeft]
        result[PlayerMoveState.JumpRight] = self._animations[AnimationNames.JumpRight]
        result[PlayerMoveState.JumpUp] = self._animations[AnimationNames.JumpUp]
        result[PlayerMoveState.Standing] = self._animations[AnimationNames.Standing]
        result[PlayerMoveState.StandingLeft] = self._animations[AnimationNames.StandingLeft]
        result[PlayerMoveState.StandingRight] = self._animations[AnimationNames.StandingRight]
        return result

    def configureAnimations(self, configuration):
        """Configure the animation from config file."""
        defaultAnimations = self.animationList()

        for aniName in defaultAnimations:
            if aniName in configuration:
                self._animations[aniName] = self.loadAnimationFromConfiguration(aniName, configuration[aniName])
            else:
                logging.warn("Animation: {0} in player configuration.".format(aniName))
        self._stateToAnimationMapper = self.getAnimationMapping()
        pass

    def loadAnimationFromConfiguration(self, animationname, configuration):
        result = AnimationInfo()
        result.configure(self._spriteName, animationname, configuration)
        return result


    def configureProperties(self, properties):
        pass

    def joystickChanged(self, joystick):
        """Handle the joystick event."""
        self._moveStateMachine.joystickChanged(joystick)
        pass

    def _getImage(self, moveState, time, position):
        """Get the subsurface of the animation based on moveState and time."""
        result = None
        ani = self._stateToAnimationMapper[moveState]
        self.rect.left = position.left
        self.rect.top = position.top
        if ani:
            result = ani.getImageFromAnimation(time, position)
        return result


    def update(self, *args):
        """Updates the players image and position."""
        ticks = pygame.time.get_ticks()
        self._positionUpdater.updatePosition(ticks, self._moveStateMachine.moveState)
        self._moveStateMachine.updateState(ticks)
        self.image = self._getImage(self._moveStateMachine.moveState, ticks, self._viewPointer.playerOffset)

        return super().update(*args)

    def savePosition(self, time):
        self._moveStartTime = time
        self._moveStartPosition = (self.x, self.y)
        pass

    def updatePosition(self, time, moveState):
        self._positionUpdater.updatePosition(time, moveState)
        pass
    
    @property
    def x(self):
        return self._viewPointer.playerPositionX
    @x.setter
    def x(self, value):
        self._viewPointer.playerPositionX = value
        pass

    @property
    def y(self):
        return self._viewPointer.playerPositionY
    @y.setter
    def y(self, value):
        self._viewPointer.playerPositionY = value

    @property
    def collideRect(self):
        return self._collideRect

    @collideRect.setter
    def collideRect(self, value):
        self._collideRect = value

    @property
    def moveCalculator(self):
        return self._moveCalculator

    @property
    def moveStartInfo(self):
        return (self._moveStartTime, self._moveStartPosition)



     


