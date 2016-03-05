from Utils.sprites.SpriteBase import SpriteMoveState
from Utils.sprites.SpriteIntelligenceBase import SpriteIntelligenceBase
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.ViewPointer import ViewPoint
from Tiled.TiledSpriteCollider import TiledSpriteCollider, TileTouchState, CollisionResult

class BackAndForthIntelligence(SpriteIntelligenceBase):
    """The sprite moves to one direction until it is stopped by a wall or a abyss.
    Then it changes the direction until it is stopped again."""

    def __init__(self, parentSprite, properties):
        self._map = ServiceLocator.getGlobalServiceInstance(ServiceNames.Map)
        self._collider = TiledSpriteCollider()
        #self._moveState = SpriteMoveState.MoveLeft
        parentSprite.moveState = SpriteMoveState.MoveLeft
        self._walkSpeed = 0.1
        self._lastPosition = None
        self._lastChange = None
        self._maxMoveTime = None

        return super().__init__(parentSprite, properties)

    def calcWalking(self, time):
        return int(time * self._walkSpeed)

    def calculateMoveTime(self, sprite, moveState):
        result = None
        offset = sprite.position
        rect = sprite.collideRect
        abort = False
        time = 0
        while not abort:
            time += 10
            x = self.calcWalking(time)
            if moveState == SpriteMoveState.MoveLeft:
                position = ViewPoint(offset.left - x, offset.top)
                state = self._collider.checkCollideAt(self._map, rect, position)
                if state.isLeftTouched or state.isStandingOnEdge or time >= 15000:
                    abort = True
                    result = (time, position)

            elif moveState == SpriteMoveState.MoveRight:
                position = ViewPoint(offset.left + x, offset.top)
                state = self._collider.checkCollideAt(self._map, rect, position)
                state.BottomLeft.StateVertical
                if state.isRightToched or state.isStandingOnEdge or time > 15000:
                    abort = True
                    result = (time, position)

        return result

    def _changeToDirection(self, sprite, time, direction):
        sprite.moveState = direction
        self._maxMoveTime = self.calculateMoveTime(sprite, direction)
        self._lastChange = time
        self._lastPosition = sprite.position
        pass


    def updatePosition(self, sprite, time):
        ##########
        # Calculate the move state
        ##########
        if not self._lastChange:
            self._changeToDirection(sprite, time, sprite.moveState)

        if sprite.moveState == SpriteMoveState.MoveLeft:
            if not self._maxMoveTime:
                self._maxMoveTime = self.calculateMoveTime(sprite, SpriteMoveState.MoveLeft)
            if time - self._lastChange >= self._maxMoveTime[0]:
                # Maximum time move reached
                sprite.x = self._maxMoveTime[1].left
                self._changeToDirection(sprite, time, SpriteMoveState.MoveRight)
        elif sprite.moveState == SpriteMoveState.MoveRight:
            if not self._maxMoveTime:
                self._maxMoveTime = self.calculateMoveTime(sprite, SpriteMoveState.MoveRight)
            if time - self._lastChange >= self._maxMoveTime[0]:
                # Maximum time move reached
                sprite.x = self._maxMoveTime[1].left
                self._changeToDirection(sprite, time, SpriteMoveState.MoveLeft)

        #################
        # Move the sprite
        #################
        
        if sprite.moveState == SpriteMoveState.MoveRight:
            vector = 1
        else:
            vector = -1
        duration = time - self._lastChange
        move = self.calcWalking(duration) * vector
        sprite.x = self._lastPosition.left + move


        return super().updatePosition(sprite, time)


