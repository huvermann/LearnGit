from Utils.JoystickStates import JoystickEvents, JoystickState
from Utils.MapPosition import MapPosition

class PlayerMoveState(object):
    Standing = 1
    Falling = 2
    MoveLeft = 3
    MoveRight = 4
    JumpLeft = 5
    JumpRight = 6
    Dying = 7
    Killed = 8
    invisible = 9

class MoveVector(object):
    X = 0
    Y = 0


class PlayerMoveStateMachine(object):
    """description of class"""
    def __init__(self, **kwargs):
        self._moveState = PlayerMoveState.Standing
        self._joystickState = JoystickState()
        self._lastChange = None
        self._lastPosition = None
        self._getTileInfoCallback = None
        self._getCurrentPositionCallback = None
        return super().__init__(**kwargs)

    def getVectors(self, moveState):
        """Returns moving vectors depending on move state."""
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

    @property
    def currentPositionCallback(self):
        return self._getCurrentPositionCallback
    @currentPositionCallback.setter
    def currentPositionCallback(self, value):
        self._getCurrentPositionCallback = value


    def joystickChanged(self, state):
        self._joystickState.joystickChanged(state)
        pass

    def _isPlayerGrounded(self):
        result = True
        if self._getTileInfoCallback:
            info = self._getTileInfoCallback()
            #todo: info auswerten, ob Spieler Bodenkontakt hat.
        return result

    def _isBarrierLeft(self):
        """Checks if barrier on the left."""
        #todo: implement
        return False

    def _isBarrierRight(self):
        """Checks if barrier on the left."""
        #todo: implement
        return False

    def _isBarrierTopLeft():
        #todo: implement
        return False
    def _isBarrierTopRight():
        #todo: implement
        return False

    def updateState(self, timeStamp):
        """Updates and returns the move state."""
        if self._moveState == PlayerMoveState.Standing:
            self._checkStanding(timeStamp)
        elif self._moveState == PlayerMoveState.Falling:
            self._checkFalling(timeStamp)
        elif self._moveState == PlayerMoveState.MoveLeft:
            self._checkMoveLeft(timeStamp)
        elif self._moveState == PlayerMoveState.MoveRight:
            self._checkMoveRight(timeStamp)
        elif self._moveState == PlayerMoveState.JumpLeft:
            self._checkJumpLeft(timeStamp)
        elif self._moveState == PlayerMoveState.JumpRight:
            self._checkJumpRight(timeStamp)
        return self._moveState

    def _checkStanding(self, timeStamp):
        """Checks if the move state must be changed."""
        if not self._isPlayerGrounded():
            self._changeToFalling()
        elif self._joystickState.keyState == JoystickEvents.MoveLeft:
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
        if self._isPlayerGrounded():
            self._changeToStanding(timeStamp)
        pass

    def _checkMoveLeft(self, timeStamp):
        """Checks if the move state must be changed."""
        if self._isBarrierLeft():
            self._changeToStanding(timeStamp)
        elif not self._isPlayerGrounded():
            self._changeToFalling(timeStamp)
        elif self._joystickState.keyState == JoystickEvents.MoveRight:
            self._changeToDirection(JoystickEvents.MoveRight, timeStamp)
        elif self._joystickState.keyState == JoystickEvents.KeyReleased:
            self._changeToStanding(timeStamp)

        pass
    def _checkMoveRight(self, timeStamp):
        """Checks if the move state must be changed."""
        if self._isBarrierRight():
            self._changeToStanding(timeStamp)
        elif self._joystickState.keyState == JoystickEvents.MoveLeft:
            self._changeToDirection(JoystickEvents.MoveLeft, timeStamp)
        elif self._joystickState.keyState == JoystickEvents.KeyReleased:
            self._changeToStanding(timeStamp)
        pass

    def _checkJumpLeft(self, timeStamp):
        """Checks if the move state must be changed."""
        if self._isBarrierTopLeft():
            self._changeToStanding(timeStamp)
        #todo: check jump finished
        pass
    def _checkJumpRight(self, timeStamp):
        """Checks if the move state must be changed."""
        if self._isBarrierTopRight():
            self._changeToStanding(timeStamp)
        #todo: check jump finished
        pass

    def _saveTimePosition(self, timeStamp):
        self._lastChange = timeStamp
        if self.currentPositionCallback:
            self._lastPosition = self.currentPositionCallback()
        pass

    def _changeToFalling(self, timeStamp):
        """Changes into falling mode."""
        self._saveTimePosition(timeStamp)
        self._moveState = PlayerMoveState.Falling
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
        self._moveState = PlayerMoveState.JumpLeft

    def _changeToStanding(self, timeStamp):
        """Changes to standing mode."""
        self._saveTimePosition(timeStamp)
        self._lastChange = None
        self._moveState = PlayerMoveState.Standing


    @property
    def moveState(self):
        return self._moveState



