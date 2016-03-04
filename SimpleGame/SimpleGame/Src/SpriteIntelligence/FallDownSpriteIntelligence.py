from Utils.sprites.SpriteIntelligenceBase import SpriteIntelligenceBase, SpriteMoveState
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Tiled.TiledSpriteCollider import TiledSpriteCollider, TileTouchState, CollisionResult
from Utils.JumpCalculator import JumpCalculator
from Utils.ViewPointer import ViewPoint

class FallDownSpriteIntelligence(SpriteIntelligenceBase):
    """This sprite is just intelligent enough to fall down on the ground. Wow!"""
    def __init__(self, parentSprite):
        self._map = ServiceLocator.getGlobalServiceInstance(ServiceNames.Map)
        self._collider = TiledSpriteCollider()
        self._moveState = SpriteMoveState.Standing
        self._moveCalculator = JumpCalculator(fallSpeed = 0.2)
        self._lastPosition = None
        self._lastChange = None

        return super().__init__(parentSprite)

    def calculateMaxFallingTime(self, sprite):
        result = None
        offset = sprite.position
        rect = sprite.collideRect
        abort = False
        time = 0
        while not abort:
            time += 1
            y = self._moveCalculator.calcFalling(time)
            position = ViewPoint(offset.left, offset.top + y)
            state = self._collider.checkCollideAt(self._map, rect, position)
            if state.isGrounded:
                result = (time, position)
                abort = True
            elif time > 5000:
                result = (5000, position)

        return result

    def _changeToStandingState(self, sprite, time):
        self._lastChange = None
        self._lastPosition = None
        self._maxMoveTime = None
        self._moveState = SpriteMoveState.Standing
        pass

    def _changeToFallingState(self, sprite, time):
        self._lastChange = time
        self._lastPosition = sprite.position
        self._maxMoveTime = self.calculateMaxFallingTime(sprite)
        self._moveState = SpriteMoveState.FallingDown
        pass

    def updatePosition(self, sprite, time):
        # Check if this sprite is grounded.
        field = self._collider.checkCollideAt(self._map, sprite.collideRect, sprite.position)
        if self._moveState == SpriteMoveState.FallingDown:
            if not self._maxMoveTime:
                self._maxMoveTime = self.calculateMaxFallingTime(sprite)
            
            if time - self._lastChange >= self._maxMoveTime[0]:
                # Maximum falling time reached
                sprite.y = self._maxMoveTime[1].top
                self._changeToStandingState(sprite, time)

            #elif field.isGrounded:
            #    self._changeToStandingState(sprite, time)
        elif self._moveState == SpriteMoveState.Standing:
            if not field.isGrounded:
                self._changeToFallingState(sprite, time)
        if self._moveState == SpriteMoveState.FallingDown:
            duration = time - self._lastChange
            move = self._moveCalculator.calcFalling(duration)
            sprite.y = self._lastPosition.top + move

        return super().updatePosition(sprite, time)

