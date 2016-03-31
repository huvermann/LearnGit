from Utils.player.PlayerMoveState import PlayerMoveState
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.JoystickStates import JoystickEvents
from Tiled.MapScanner import MapScanner
import pygame

class MoveStateMachine(object):
    """Player Move State Machine."""
    def __init__(self, parent):
        self._parent = parent
        self._joystickState = None
        self._lastJoystickMove = None
        self._moveCalculator = parent.moveCalculator
        self._moveState = PlayerMoveState.Standing
        currentMap = ServiceLocator.getGlobalServiceInstance(ServiceNames.Map)
        self._mapScanner = MapScanner(currentMap, parent)
        self._targetPosition = None
        
        pass

    def joystickChanged(self, joystick):
        """Joystick state has been changed."""
        time = pygame.time.get_ticks()
        self._lastJoystickMove = time
        self._lastJoystickMove = joystick
        
        self.updateState(time, joystick)
        pass

    def updateState(self, ticks, joystick = None):
        """Check if the move state has changed."""
        if self._moveState in [PlayerMoveState.Standing, PlayerMoveState.StandingLeft, PlayerMoveState.StandingRight]:
            self._checkStanding(ticks, joystick)
        elif self._moveState in [PlayerMoveState.Falling, PlayerMoveState.FallingLeft, PlayerMoveState.FallingRight]:
            self._checkFalling(ticks)
        elif self._moveState in [PlayerMoveState.MoveLeft, PlayerMoveState.MoveRight]:
            self._checkMoving(ticks, joystick)
        elif self._moveState in [PlayerMoveState.JumpLeft, PlayerMoveState.JumpRight, PlayerMoveState.JumpUp]:
            self._checkJumping(ticks)
        elif self._moveState in [PlayerMoveState.ClimbDown, PlayerMoveState.ClimbUp]:
            self._checkClimbing(ticks)
        pass

    def _checkStanding(self, time, joystick):
        if self._mapScanner.getWayToGround() > 1:
            print(self._mapScanner.getWayToGround())
            self._changeToFalling(time)

        if joystick != None:
            if joystick in [JoystickEvents.MoveLeft, JoystickEvents.MoveRight]:
                self._changeToMoving(time, joystick)

        pass

    def _checkFalling(self, time):
        
        print("CheckFalling")
        if time >= self._targetPosition[0]:
            # Sprite reached point

            self._changeToStanding(time)
        pass

    def _checkMoving(self, time, joystick):
        print("Check moving")
        if joystick != None:
            if joystick == JoystickEvents.KeyReleased:
                # Update the position
                self._parent.updatePosition(time, self._moveState)
                self._moveState = PlayerMoveState.Standing

            if joystick == JoystickEvents.JumpButton:
                
                self._changeToJumping(time, joystick)
        #Todo: check if player can fall down
        #Todo: check if player crashes into wall
        pass

    def _checkJumping(self, time):
        # check if timeout
        # if timeout update position and  set state to standing
        pass

    def _checkClimbing(self, time):
        pass

    def savePosition(self, time):
        self._parent.savePosition(time)
        pass

    def _changeToFalling(self, time):
        #Calculate falling time
        def calculateBounce(time, sprite):
            fallspeed = sprite.moveCalculator.fallSpeed / 1000
            down = int(self._mapScanner.getWayToGround())
            falltime = int(down // fallspeed)
            result = (time + falltime, (sprite.x, sprite.y + down))
            return result
        
        self.savePosition(time)
        self._targetPosition = calculateBounce(time, self._parent)

        self._moveState = PlayerMoveState.Falling
        pass

    def _changeToStanding(self, time):
        self._parent.x = self._targetPosition[1][0]
        self._parent.y = self._targetPosition[1][1]
        self._targetPosition = None
        self._moveState = PlayerMoveState.Standing
        pass

    def _changeToMoving(self, time, joystick):
        self._parent.updatePosition(time, self._moveState)
        self._parent.savePosition(time)
        if joystick == JoystickEvents.MoveLeft:
            self._moveState = PlayerMoveState.MoveLeft
        elif joystick == JoystickEvents.MoveRight:
            self._moveState = PlayerMoveState.MoveRight
        pass

    def _changeToJumping(self, time, joystick):
        # update latest position
        self._parent.updatePosition(time, self._moveState)
        #Calculate the jump
        #Change the move state
        pass







    @property
    def moveState(self):
        return self._moveState
    @moveState.setter
    def moveState(self, value):
        self._moveState = value




