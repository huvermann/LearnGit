from Utils.JoystickStates import JoystickEvents, JoystickState
from Utils.Constants import Corners
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.ViewPointer import ViewPointer, ViewPoint
from Tiled.TiledSpriteCollider import TiledSpriteCollider, CollisionResult, CollisionDetail, TileTouchState
from Utils.player.MoveTimeCalculator import MoveTimeCalculator
from Utils.JumpCalculator import JumpCalculator, JumpSizeMode
import pygame


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
    ClimbUp = 12
    ClimbDown = 13
    Dying = 14
    Killed = 15
    invisible = 16



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
        self._MoveEndFlag = None
        self._getTileInfoCallback = None
        self._getCurrentPositionCallback = None
        self._jumpTimeout = 100
        self._jumpSize = None
        
        self._backgroundTiles = [0, 28, 29, 30, 31]
        self.__viewPoint = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewPointer)
        self.__collider = TiledSpriteCollider()

        
        self._moveTimeCalculator = MoveTimeCalculator(self.__viewPoint, self.__collider, parentPlayer._JumpCalculator)
        #ServiceLocator.registerGlobalService(ServiceNames.TiledWatcher, self.__tileWatcher)
    
    def getVectors(self, moveState):
        """Returns moving vectors depending on move state."""
        # Obsolete remove it!
        result = MoveVector()
        if moveState == PlayerMoveState.MoveLeft:
            result.X = -1
        elif moveState == PlayerMoveState.JumpLeft:
            result.X = -1
        elif moveState == PlayerMoveState.MoveRight:
            result.X = 1
        elif moveState == PlayerMoveState.JumpRight:
            result.X = 1
        elif moveState == PlayerMoveState.Falling:
            result.X = 0
            result.Y = 1
        #Todo: Implement vector for jumping
        return result

    def reset(self):
        self._changeToStanding(pygame.time.get_ticks())
        pass


    def joystickChanged(self, state):
        self._joystickState.joystickChanged(state)
        pass

    def updateState(self, timeStamp):
        """Updates and returns the move state."""
        self.__collider.setPlayerPosition(self.__viewPoint.getPlayerMapPosition())
        if self._moveState in [PlayerMoveState.Standing, PlayerMoveState.StandingLeft, PlayerMoveState.StandingRight]:
            self._checkStanding(timeStamp)
        elif self._moveState in [PlayerMoveState.Falling, PlayerMoveState.FallingLeft, PlayerMoveState.FallingRight]:
            self._checkFalling(timeStamp)

        elif self._moveState in [PlayerMoveState.MoveLeft, PlayerMoveState.MoveRight]:
            self._checkMove(timeStamp)

        elif self._moveState in [PlayerMoveState.JumpLeft, PlayerMoveState.JumpRight, PlayerMoveState.JumpUp]:
            self._checkJump(timeStamp)

        if self._moveState in [PlayerMoveState.ClimbUp, PlayerMoveState.ClimbDown]:
            self._checkClimb(timeStamp)

        return self._moveState

    def _checkStanding(self, timeStamp):
        """Checks if the move state must be changed."""
        #if not self.__tileWatcher.isBarrierOn(CheckDirection.Ground):
        if not self.__collider.currentState.isGrounded:
            self._changeToFalling(timeStamp)
        elif self._joystickState.keyState in [JoystickEvents.MoveLeft, JoystickEvents.MoveRight]:
            self._changeToDirection(self._joystickState.keyState, timeStamp)
        elif self._joystickState.buttonState == JoystickEvents.JumpButton:
            self._changeToJumping(timeStamp)
        elif self._joystickState.keyState == JoystickEvents.MoveUp:
            if self.__collider.currentState.isLadderTouched:
                self._changeToClimbing(timeStamp)
            else:
                self._moveState = PlayerMoveState.Standing
        elif self._joystickState.keyState == JoystickEvents.MoveDown:
            if self.__collider.currentState.isLadderTouched:
                self._changeToClimbing(timeStamp)

        #impl: self._joystickState == JoystickEvents.MoveDown:
        pass

    def _checkClimb(self, timeStamp):
        if self._joystickState.keyState == JoystickEvents.KeyReleased:
            self._changeToStanding(timeStamp)
        elif not self.__collider.currentState.isGrounded:
            self._changeToFalling(timeStamp)
        elif self._joystickState.keyState in [JoystickEvents.MoveLeft, JoystickEvents.MoveRight]:
            self._changeToDirection(self._joystickState.keyState, timeStamp)
        elif self._joystickState.buttonState == JoystickEvents.JumpButton:
            self._changeToJumping(timeStamp)
        elif self._joystickState.keyState == JoystickEvents.MoveDown and self._moveState == PlayerMoveState.ClimbUp:
            self._changeToClimbing(timeStamp)
        elif self._joystickState.keyState == JoystickEvents.MoveUp and self._moveState == PlayerMoveState.ClimbDown:
            self._changeToClimbing(timeStamp)
        elif self._moveState == PlayerMoveState.ClimbDown and not self.__collider.currentState.isLadderOnFeeds:
            self._changeToStanding(timeStamp)
        pass

    def _changeToClimbing(self, timeStamp):
        self._saveTimePosition(timeStamp)
        if self._joystickState.keyState == JoystickEvents.MoveUp:
            self._moveState = PlayerMoveState.ClimbUp
        elif self._joystickState.keyState == JoystickEvents.MoveDown:
            self._moveState = PlayerMoveState.ClimbDown
        pass

    def _checkFalling(self, timeStamp):
        """Checks if the move state must be changed."""
        #if self.__tileWatcher.isBarrierOn(CheckDirection.Ground):
        if self.__collider.currentState.isGrounded:
            self._changeToStanding(timeStamp)
        elif self._joystickState.keyState in [JoystickEvents.MoveLeft, JoystickEvents.MoveRight]:
            self._manipulateWhileFalling(timeStamp)
        elif timeStamp >= self.lastChange + self.moveTimeLimit[0]: # Check if move has ended.
            self.lastChange = None
            self._MoveEndFlag = self.moveTimeLimit # the update mechanism must handle the flag.
            self._changeToStanding(timeStamp)

        pass

    def _checkMove(self, timeStamp):
        """Checks if the move state must be changed."""
        if self.moveTimeLimit and timeStamp >= self.lastChange + self.moveTimeLimit[0]:
            self._changeToStanding(timeStamp)
        #if not self.__tileWatcher.isBarrierOn(CheckDirection.Ground):
        if not self.__collider.currentState.isGrounded:
            self._changeToFalling(timeStamp)
        elif self._moveState == PlayerMoveState.MoveLeft:
            #check left
            if self._joystickState.keyState == JoystickEvents.MoveRight:
                # Move right
                self._changeToDirection(JoystickEvents.MoveRight, timeStamp)
            elif self._joystickState.buttonState == JoystickEvents.JumpButton:
                # Jump left
                self._changeToJumping(timeStamp)
            elif self._joystickState.keyState == JoystickEvents.MoveUp:
                self._changeToStanding(timeStamp)
            elif self._joystickState.keyState == JoystickEvents.KeyReleased:
                #self._changeToStanding(timeStamp)
                self._moveWhileKeyRelease(timeStamp)
            #elif self.__tileWatcher.isBarrierOn(CheckDirection.Left):
            elif self.__collider.currentState.isLeftTouched:
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
                #self._changeToStanding(timeStamp)
                self._moveWhileKeyRelease(timeStamp)
            #elif self.__tileWatcher.isBarrierOn(CheckDirection.Right):
            elif self.__collider.currentState.isRightToched:
                self._changeToStanding(timeStamp) 

        pass

    def _moveWhileKeyRelease(self, timeStamp):
        """User releases the key while moving left or right."""
        movetime = self._joystickState.lastChange - self.lastChange
        way = self._moveTimeCalculator.calculateHorizontalMove(movetime)
        vector = self.getVectors(self._moveState)
        position = self._lastPosition.copy()
        position.left += way * vector.X
        self._moveTimeLimit = (movetime, position)
        self._MoveEndFlag = self._moveTimeLimit
        print("MoveWhileKeyRelease: {0} pixel, time: {1}".format(way * vector.X, movetime))
        pass

    def _checkJump(self, timeStamp):
        """Checks if the move state must be changed."""
        if timeStamp >= self.lastChange + self.moveTimeLimit[0]: # Check if move has ended.
            self.lastChange = None
            self._MoveEndFlag = self.moveTimeLimit # the update mechanism must handle the flag.
            self._changeToStanding(timeStamp)
        pass

    def _saveTimePosition(self, timeStamp):
        self._lastChange = timeStamp
        self._lastPosition = self.__viewPoint.getPlayerMapPosition()
        self._moveTimeLimit = None
        pass

    def _changeToFalling(self, timeStamp):
        """Changes into falling mode."""
        self._saveTimePosition(timeStamp)
        if self._moveState in [PlayerMoveState.Standing, PlayerMoveState.JumpUp]:
            self._moveState = PlayerMoveState.Falling
        elif self._moveState in [PlayerMoveState.JumpLeft, PlayerMoveState.MoveLeft, PlayerMoveState.StandingLeft]:
            self._moveState = PlayerMoveState.FallingLeft
        elif self._moveState in [PlayerMoveState.JumpRight, PlayerMoveState.MoveRight, PlayerMoveState.StandingRight]:
            self._moveState = PlayerMoveState.FallingRight
        else:
            self._moveState = PlayerMoveState.Falling

        self._moveTimeLimit = self.calculateMaxFallTime(timeStamp)

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
            if self._moveState == PlayerMoveState.StandingLeft:
                self.changeJumpSize(JumpSizeMode.Short)
            else:
                self.changeJumpSize(JumpSizeMode.Long)
            self._moveState = PlayerMoveState.JumpLeft
           
            self._moveTimeLimit = self._calculateMaxJumpTime(timeStamp, self.moveState)
        elif self._moveState in [PlayerMoveState.FallingRight, PlayerMoveState.MoveRight, PlayerMoveState.StandingRight]:
            if self._moveState == PlayerMoveState.StandingRight:
                self.changeJumpSize(JumpSizeMode.Short)
            else:
                self.changeJumpSize(JumpSizeMode.Long)
            self._moveState = PlayerMoveState.JumpRight
            self._moveTimeLimit = self._calculateMaxJumpTime(timeStamp, self.moveState)
        else:
            #Todo: Kleiner Sprung aktivieren
            self.changeJumpSize(JumpSizeMode.Short)
            self._calculateMaxJumpUpTime(timeStamp)
            self._moveTimeLimit = self._calculateMaxJumpUpTime(timeStamp)
            self._moveState = PlayerMoveState.JumpUp
        pass

    def _calculateMaxJumpTime(self, timeStamp, moveState):
        """Calculates the maximum jump time."""
        return self._moveTimeCalculator.calculateJumpTime(self.getVectors(moveState))

    def _calculateMaxJumpUpTime(self, timeStamp):
        """Calculates the maximum jump time for jump up."""
        #Todo: Implement the calculation.
        return self._moveTimeCalculator.calculateMaxJumpUpTime()

    def calculateMaxFallTime(self, timestamp):
        return self._moveTimeCalculator.calculateMaximumFallDownTime()

    def changeJumpSize(self, jumpSize):
        """Change the jump size."""
        assert jumpSize == 0 or jumpSize == 1, "JumpSitze must be JumpSizeMode.Short or JumpSizeMode.Long."
        #ServiceLocator.getGlobalServiceInstance(ServiceNames.Player).jumpCalculator.horizontalJumpSize = jumpSize
        player = ServiceLocator.getGlobalServiceInstance(ServiceNames.Player)
        calculator = player.jumpCalculator
        calculator.horizontalJumpSize = jumpSize


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
    def collider(self):
        return self.__collider

    @property
    def jumpSize(self):
        return self._jumpSize



