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
        self._moveTimeLimit = None
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



    def joystickChanged(self, state):
        self._joystickState.joystickChanged(state)
        pass

    def updateState(self, timeStamp):
        """Updates and returns the move state."""
        if self._moveState in [PlayerMoveState.Standing, PlayerMoveState.StandingLeft, PlayerMoveState.StandingRight]:
            self._checkStanding(timeStamp)
        elif self._moveState in [PlayerMoveState.Falling, PlayerMoveState.FallingLeft, PlayerMoveState.FallingRight]:
            self._checkFalling(timeStamp)

        elif self._moveState in [PlayerMoveState.MoveLeft, PlayerMoveState.MoveRight]:
            self._checkMove(timeStamp)

        elif self._moveState in [PlayerMoveState.JumpLeft, PlayerMoveState.JumpRight, PlayerMoveState.JumpUp]:
            self._checkJump(timeStamp)

        return self._moveState

    def _checkStanding(self, timeStamp):
        """Checks if the move state must be changed."""
        if not self.__tileWatcher.isBarrierOn(CheckDirection.Ground):
            self._changeToFalling(timeStamp)
        elif self._joystickState.keyState in [JoystickEvents.MoveLeft, JoystickEvents.MoveRight]:
            self._changeToDirection(self._joystickState.keyState, timeStamp)
        elif self._joystickState.buttonState == JoystickEvents.JumpButton:
            self._changeToJumping(timeStamp)
        elif self._joystickState.keyState == JoystickEvents.MoveUp:
            self._moveState = PlayerMoveState.Standing
        #impl: self._joystickState == JoystickEvents.MoveDown:
        pass

    def _checkFalling(self, timeStamp):
        """Checks if the move state must be changed."""
        if self.__tileWatcher.isBarrierOn(CheckDirection.Ground):
            self._changeToStanding(timeStamp)
        elif self._joystickState.keyState in [JoystickEvents.MoveLeft, JoystickEvents.MoveRight]:
            self._manipulateWhileFalling(timeStamp)
        pass

    def _checkMove(self, timeStamp):
        """Checks if the move state must be changed."""
        if not self.__tileWatcher.isBarrierOn(CheckDirection.Ground):
            self._changeToFalling(timeStamp)
        elif self._moveState == PlayerMoveState.MoveLeft:
            #check left
            if self._joystickState.keyState == JoystickEvents.MoveRight:
                # Move right
                self._changeToDirection(JoystickEvents.MoveRight, timeStamp)
            elif self._joystickState.keyState == JoystickEvents.JumpButton:
                # Jump left
                self._changeToJumping(timeStamp)
            elif self._joystickState.keyState == JoystickEvents.MoveUp:
                self._changeToStanding(timeStamp)
            elif self._joystickState.keyState == JoystickEvents.KeyReleased:
                self._changeToStanding(timeStamp)
            elif self.__tileWatcher.isBarrierOn(CheckDirection.Left):
                self._changeToStanding(timeStamp)

            
        elif self._moveState == PlayerMoveState.MoveRight:
            #check move right
            if self._joystickState.keyState == JoystickEvents.MoveLeft:
                # Turn around left
                self._changeToDirection(JoystickEvents.MoveLeft, timeStamp)
            elif self._joystickState.buttonState == JoystickEvents.JumpButton:
                #Jump right
                self._changeToJumping(timeStamp)
            elif self._joystickState.keyState == JoystickEvents.MoveUp:
                self._changeToStanding(timeStamp)
            elif self._joystickState.keyState == JoystickEvents.KeyReleased:
                self._changeToStanding(timeStamp)
            elif self.__tileWatcher.isBarrierOn(CheckDirection.Right):
                self._changeToStanding(timeStamp) 

        pass

    def _checkJump(self, timeStamp):
        """Checks if the move state must be changed."""
        if self.__tileWatcher.isBarrierOn(CheckDirection.Top):
            self._changeToFalling(timeStamp)
        elif self._moveState == PlayerMoveState.JumpLeft:

            if self.__tileWatcher.isBarrierOn(CheckDirection.Left) or self.__tileWatcher.isBarrierOn(CheckDirection.Top) or self.__tileWatcher.isBarrierOn(CheckDirection.TopLeft):
                self._changeToFalling(timeStamp)
            elif self._moveTimeLimit < timeStamp - self._lastChange:
                self._changeToFalling(timeStamp)

        elif self._moveState == PlayerMoveState.JumpRight:
            if self.__tileWatcher.isBarrierOn(CheckDirection.Right) or self.__tileWatcher.isBarrierOn(CheckDirection.Top) or self.__tileWatcher.isBarrierOn(CheckDirection.TopRight):
                self._changeToFalling(timeStamp)
            elif self._moveTimeLimit < timeStamp - self._lastChange:
                self._changeToFalling(timeStamp)

        elif self._moveState == PlayerMoveState.JumpUp:
            if self.__tileWatcher.isBarrierOn(CheckDirection.Top):
                self._changeToFalling(timeStamp)

        pass

    def _saveTimePosition(self, timeStamp):
        self._lastChange = timeStamp
        self._lastPosition = self.__viewPoint.getPlayerMapPosition()
        self._moveTimeLimit = None
        pass

    def _changeToFalling(self, timeStamp):
        """Changes into falling mode."""
        print("Change to falling")
        self._saveTimePosition(timeStamp)
        if self._moveState in [PlayerMoveState.Standing, PlayerMoveState.JumpUp]:
            self._moveState = PlayerMoveState.Falling
        elif self._moveState in [PlayerMoveState.JumpLeft, PlayerMoveState.MoveLeft, PlayerMoveState.StandingLeft]:
            self._moveState = PlayerMoveState.FallingLeft
        elif self._moveState in [PlayerMoveState.JumpRight, PlayerMoveState.MoveRight, PlayerMoveState.StandingRight]:
            self._moveState = PlayerMoveState.FallingRight
        else:
            self._moveState = PlayerMoveState.Falling

        pass

    def _changeToDirection(self, direction, timeStamp):
        """Changes to walking mode."""
        print ("Change to Walking")
        self._saveTimePosition(timeStamp)
        if direction == JoystickEvents.MoveLeft:
            self._moveState = PlayerMoveState.MoveLeft
        elif direction == JoystickEvents.MoveRight:
            self._moveState = PlayerMoveState.MoveRight
        pass

    def _changeToJumping(self, timeStamp):
        """Changes into jumping mode."""
        print("change to jumping")
        self._saveTimePosition(timeStamp)
        if self._moveState in [PlayerMoveState.FallingLeft, PlayerMoveState.MoveLeft, PlayerMoveState.StandingLeft]:
            self._moveState = PlayerMoveState.JumpLeft
        elif self._moveState in [PlayerMoveState.FallingRight, PlayerMoveState.MoveRight, PlayerMoveState.StandingRight]:
            self._moveState = PlayerMoveState.JumpRight
        else:
            self._moveState = PlayerMoveState.JumpUp
        pass

    def _changeToStanding(self, timeStamp):
        """Changes to standing mode."""
        print("Change to standing")
        self._saveTimePosition(timeStamp)
        self._lastChange = None

        if self._moveState in [PlayerMoveState.FallingLeft, PlayerMoveState.JumpLeft, PlayerMoveState.MoveLeft]:
            self._moveState = PlayerMoveState.StandingLeft
        elif self._moveState in [PlayerMoveState.FallingRight, PlayerMoveState.JumpRight, PlayerMoveState.MoveRight]:
            self._moveState = PlayerMoveState.StandingRight
        else:
            self._moveState = PlayerMoveState.Standing
        pass

    def _manipulateWhileFalling(self, timeStamp):
        """Manipulate the fly while falling."""
        #Todo: Implement.
        pass

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
    def moveState(self):
        return self._moveState

    @property
    def moveTimeLimit(self):
        return self._moveTimeLimit
    @moveTimeLimit.setter
    def moveTimeLimit(self, value):
        self._moveTimeLimit = value

    @property
    def tilesWatcher(self):
        return self.__tileWatcher



