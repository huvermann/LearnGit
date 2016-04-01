from Utils.player.PlayerMoveState import PlayerMoveState

class PlayerPositionUpdater(object):
    """Updates the players position."""
    
    def __init__(self, player, viewPointer):
        self._player = player
        self._viewPointer = viewPointer
        pass

    def updatePosition(self, time, moveState):
        """Updates the players position."""

        if moveState in [PlayerMoveState.MoveLeft, PlayerMoveState.MoveRight]:
            print("Move")
            self._moveLeftRight(time, moveState)

        elif moveState in [PlayerMoveState.Falling, PlayerMoveState.FallingLeft, PlayerMoveState.FallingRight]:
            
            self._falling(time, moveState)

        elif moveState in []:
            self._standing(time, moveState)

        elif moveState in []:
            self._climbing(time, moveState)

        elif moveState in [PlayerMoveState.JumpLeft, PlayerMoveState.JumpRight]:
            self._jumping(time, moveState)
        pass

    def _moveLeftRight(self, time, moveState):
        if moveState == PlayerMoveState.MoveLeft:
            vector = -1
        else:
            vector = 1
        startTime, startPosition = self._player.moveStartInfo
        duration = time - startTime
        move = self._player.moveCalculator.calcWalking(duration, vector)
        self._viewPointer.playerPositionX = startPosition[0] + move
        pass

    def _falling(self, time, moveState):
        """Player falls down."""
        #calculate falling
        startTime, startPosition = self._player.moveStartInfo
        downTime = time - startTime
        down = self._player.moveCalculator.calcFalling(downTime)
        self._player.y = startPosition[1] + down
        pass

    def _standing(self, time, moveState):
        """Player stands still."""
        pass

    def _climbing(self, time, moveState):
        """Player is climbing."""
        pass

    def _jumping(self, time, moveState):
        """Player is jumping."""
        if moveState == PlayerMoveState.JumpLeft:
            vector = -1
        else:
            vector = 1

        startTime, startPosition = self._player.moveStartInfo
        duration = time - startTime
        movex = self._player.moveCalculator.calcX(duration) * vector
        movey = self._player.moveCalculator.calcY(duration)
        self._player.x = startPosition[0] + movex
        self._player.y = startPosition[1] - movey

        pass






