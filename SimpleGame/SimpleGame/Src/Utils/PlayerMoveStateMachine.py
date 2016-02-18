from Utils.JoystickStates import JoystickEvents, JoystickState
from Utils.Constants import Corners
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.ViewPointer import ViewPointer, ViewPoint
from Tiled.TiledWatcher import TiledWatcher, CheckDirection


class PlayerMoveState(object):
    Standing = 1
    StandingLeft = 2
    StandingRight = 3
    Falling = 4
    FallingLeft = 5
    FallingRight = 6
    MoveLeft = 7
    MoveRight = 8
    JumpLeft = 9
    JumpRight = 10
    JumpUp = 11
    Dying = 12
    Killed = 13
    invisible = 14

class MoveVector(object):
    X = 0
    Y = 0


class PlayerMoveStateMachine(object):
    """description of class"""
    def __init__(self, parentPlayer):
        self._moveState = PlayerMoveState.Standing
        self._joystickState = JoystickState()
        self._lastChange = None
        self._lastPosition = None
        self._getTileInfoCallback = None
        self._getCurrentPositionCallback = None
        self._jumpTimeout = 100
        self._backgroundTiles = [0, 28, 29, 30, 31]
        self.__viewPoint = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewPointer)
        self.__tileWatcher = TiledWatcher(parentPlayer)
        

    def getVectors(self, moveState):
        """Returns moving vectors depending on move state."""
        # Obsolete remove it!
        result = MoveVector()
        if moveState == PlayerMoveState.MoveLeft:
            result.X = -1
        elif moveState == PlayerMoveState.MoveRight:
            result.X = 1
        elif moveState == PlayerMoveState.Falling:
            result.X = 0
            result.Y = 1
        #Todo: Implement vector for jumping
        return result

    @property
    def jumpTimeout(self):
        return self._jumpTimeout
    @jumpTimeout.setter
    def jumpTimeout(self, value):
        self._jumpTimeout = value
    @property
    def lastChange(self):
        return self._lastChange
    @lastChange.setter
    def lastChange(self, value):
        self._lastChange = value
        pass
    @property
    def lastPosition(self):
        return self._lastPosition
    @lastPosition.setter
    def lastPosition(self, value):
        self._lastPosition = value
    

    @property
    def tileInfoCallback(self):
        return self._getTileInfoCallback
    @tileInfoCallback.setter
    def tileInfoCallback(self, value):
        self._getTileInfoCallback = value

    def joystickChanged(self, state):
        self._joystickState.joystickChanged(state)
        pass

    def _isJumpEnded(self, timeStamp):
        result = False
        if timeStamp - self._lastChange > self._jumpTimeout:
            result = True
        return result

    def updateState(self, timeStamp):
        """Updates and returns the move state."""
        if self._moveState == PlayerMoveState.Standing:
            self._checkStanding(timeStamp)
        elif self._moveState == PlayerMoveState.StandingLeft:
            self._checkStanding(timeStamp)
        elif self._moveState == PlayerMoveState.StandingRight:
            self._checkStanding(timeStamp)
        elif self._moveState == PlayerMoveState.Falling:
            self._checkFalling(timeStamp)
        elif self._moveState == PlayerMoveState.FallingLeft:
            self._checkFalling(timeStamp)
        elif self._moveState == PlayerMoveState.FallingRight:
            self._checkFalling(timeStamp)
        elif self._moveState == PlayerMoveState.MoveLeft:
            self._checkMoveLeft(timeStamp)
        elif self._moveState == PlayerMoveState.MoveRight:
            self._checkMoveRight(timeStamp)
        elif self._moveState == PlayerMoveState.JumpLeft:
            self._checkJumpLeft(timeStamp)
        elif self._moveState == PlayerMoveState.JumpRight:
            self._checkJumpRight(timeStamp)
        elif self._moveState == PlayerMoveState.JumpUp:
            self._checkJumpUp(timeStamp)
        return self._moveState

    def _checkStanding(self, timeStamp):
        """Checks if the move state must be changed."""
        if not self.__tileWatcher.isBarrierOn(CheckDirection.Ground):
            self._changeToFalling(timeStamp)
        if self._joystickState.keyState == JoystickEvents.MoveLeft:
            self._changeToDirection(JoystickEvents.MoveLeft, timeStamp)
        elif self._joystickState.keyState == JoystickEvents.MoveRight:
            self._changeToDirection(JoystickEvents.MoveRight, timeStamp)
        elif self._joystickState.keyState == JoystickEvents.MoveUp:
            self._changeToDirection(JoystickEvents.MoveUp, timeStamp)
        elif self._joystickState.keyState == JoystickEvents.MoveDown:
            self._changeToDirection(JoystickEvents.MoveDown, timeStamp)
        if self._joystickState.buttonState == JoystickEvents.JumpButton:
            self._changeToJumping(timeStamp)

        pass

    def _checkFalling(self, timeStamp):
        """Checks if the move state must be changed."""
        if self.__tileWatcher.isBarrierOn(CheckDirection.Ground):
            self._changeToStanding(timeStamp)
        pass

    def _checkMoveLeft(self, timeStamp):
        """Checks if the move state must be changed."""
        if self.__tileWatcher.isBarrierOn(CheckDirection.Left):
            self._changeToStanding(timeStamp)
        elif not self.__tileWatcher.isBarrierOn(CheckDirection.Ground):
            self._changeToFalling(timeStamp)
        elif self._joystickState.keyState == JoystickEvents.MoveRight:
            self._changeToDirection(JoystickEvents.MoveRight, timeStamp)
        elif self._joystickState.buttonState == JoystickEvents.JumpButton:
            self._changeToJumping(timeStamp)
        elif self._joystickState.keyState == JoystickEvents.KeyReleased:
            self._changeToStanding(timeStamp)

        pass
    def _checkMoveRight(self, timeStamp):
        """Checks if the move state must be changed."""
        if self.__tileWatcher.isBarrierOn(CheckDirection.Right):
            self._changeToStanding(timeStamp)
        elif not self.__tileWatcher.isBarrierOn(CheckDirection.Ground):
            self._changeToFalling(timeStamp)
        elif self._joystickState.keyState == JoystickEvents.MoveLeft:
            self._changeToDirection(JoystickEvents.MoveLeft, timeStamp)
        elif self._joystickState.buttonState == JoystickEvents.JumpButton:
            self._changeToJumping(timeStamp)
        elif self._joystickState.keyState == JoystickEvents.KeyReleased:
            self._changeToStanding(timeStamp)
        pass

    def _checkJumpLeft(self, timeStamp):
        """Checks if the move state must be changed."""
        if self.__tileWatcher.isBarrierOn(CheckDirection.TopLeft):
            self._changeToStanding(timeStamp)
        #elif self._isJumpEnded(timeStamp):
        #    self._changeToFalling(timeStamp)
        if timeStamp-self._lastChange > 50 and self.__tileWatcher.isBarrierOn(CheckDirection.Ground):
            self._changeToStanding(timeStamp)
        elif self.__tileWatcher.isBarrierOn(CheckDirection.Left):
            self._changeToStanding(timeStamp)
        pass
    def _checkJumpRight(self, timeStamp):
        """Checks if the move state must be changed."""
        if self.__tileWatcher.isBarrierOn(CheckDirection.TopRight):
            self._changeToStanding(timeStamp)
        #elif self._isJumpEnded(timeStamp):
        #    self._changeToFalling(timeStamp)
        if timeStamp-self._lastChange > 50 and self.__tileWatcher.isBarrierOn(CheckDirection.Ground):
            self._changeToStanding(timeStamp)
        elif self.__tileWatcher.isBarrierOn(CheckDirection.Right):
            self._changeToStanding(timeStamp)
        pass

    def _checkJumpUp(self, timeStamp):
        if self._isJumpEnded(timeStamp):
            self._changeToFalling(timeStamp)
        elif self.__tileWatcher.isBarrierOn(CheckDirection.Top):
            self._changeToFalling(timeStamp)


    def _saveTimePosition(self, timeStamp):
        self._lastChange = timeStamp
        self._lastPosition = self.__viewPoint.getPlayerMapPosition()
        pass

    def _changeToFalling(self, timeStamp):
        """Changes into falling mode."""
        self._saveTimePosition(timeStamp)
        if self._moveState == PlayerMoveState.StandingLeft:
            self._moveState = PlayerMoveState.FallingLeft
        elif self._moveState == PlayerMoveState.StandingRight:
            self.moveState = PlayerMoveState.FallingRight
        elif self._moveState == PlayerMoveState.JumpLeft:
            self.moveState = PlayerMoveState.FallingLeft
        elif self._moveState == PlayerMoveState.JumpRight:
            self._moveState = PlayerMoveState.FallingRight
        elif self._moveState == PlayerMoveState.MoveLeft:
            self._moveState = PlayerMoveState.FallingLeft
        elif self._moveState == PlayerMoveState.MoveRight:
            self._moveState = PlayerMoveState.FallingRight
        else:
            self._moveState = PlayerMoveState.Falling

        print("Change to falling: {0}".format(self._moveState))
        pass

    def _changeToDirection(self, direction, timeStamp):
        """Changes to walking mode."""
        self._saveTimePosition(timeStamp)
        if direction == JoystickEvents.MoveLeft:
            self._moveState = PlayerMoveState.MoveLeft
        elif direction == JoystickEvents.MoveRight:
            self._moveState = PlayerMoveState.MoveRight
        pass

    def _changeToJumping(self, timeStamp):
        """Changes into jumping mode."""
        self._saveTimePosition(timeStamp)
        if self._joystickState.keyState == JoystickEvents.MoveLeft:
            self._moveState = PlayerMoveState.JumpLeft
        elif self._joystickState.keyState == JoystickEvents.MoveRight:
            self._moveState = PlayerMoveState.JumpRight
        elif self.moveState == PlayerMoveState.StandingLeft:
            self._moveState = PlayerMoveState.JumpLeft
        elif self._moveState == PlayerMoveState.StandingRight:
            self._moveState = PlayerMoveState.JumpRight
        else :
            self._moveState = PlayerMoveState.JumpUp

    def _changeToStanding(self, timeStamp):
        """Changes to standing mode."""
        self._saveTimePosition(timeStamp)
        self._lastChange = None
        if self._moveState in [PlayerMoveState.MoveLeft, PlayerMoveState.JumpLeft, PlayerMoveState.FallingLeft]:
            self._moveState = PlayerMoveState.StandingLeft
        elif self._moveState in [PlayerMoveState.MoveRight, PlayerMoveState.JumpRight, PlayerMoveState.FallingRight]:
            self._moveState = PlayerMoveState.StandingRight
        else:
            self._moveState = PlayerMoveState.Standing


    @property
    def moveState(self):
        return self._moveState



