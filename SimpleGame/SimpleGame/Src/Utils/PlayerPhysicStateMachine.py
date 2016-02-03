from Utils.PlayerSpriteMoveState import PlayerSpriteMoveState as MoveState
class PlayerPhysicStateMachine(object):
    """Players physic state machine"""
    def __init__(self):
        self._state = MoveState.Standing
        self._startTime = None

    def calculateMove(self, position):
        """Calculates the new position based on time."""
        newPosition = position

        return newPosition
        
        


