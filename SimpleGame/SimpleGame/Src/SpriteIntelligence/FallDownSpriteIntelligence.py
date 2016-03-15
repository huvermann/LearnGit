from Utils.sprites.SpriteBase import SpriteMoveState
from Utils.sprites.SpriteIntelligenceBase import SpriteIntelligenceBase, AIPropertyNames
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Tiled.TiledSpriteCollider import TiledSpriteCollider, TileTouchState, CollisionResult
from Utils.JumpCalculator import JumpCalculator
from Utils.ViewPointer import ViewPoint

class FallDownSpriteIntelligence(SpriteIntelligenceBase):
    """This sprite is just intelligent enough to fall down on the ground. Wow!"""
    def __init__(self, parentSprite, properties):
        self._map = ServiceLocator.getGlobalServiceInstance(ServiceNames.Map)
        self._collider = TiledSpriteCollider()
        parentSprite.moveState = SpriteMoveState.Standing
        self._moveCalculator = JumpCalculator(fallSpeed = 0.1)
        self._lastPosition = None
        self._lastChange = None
        self._onSpriteHasGrounded = None

        return super().__init__(parentSprite, properties)

    def configureProperties(self, properties):
        if AIPropertyNames.FallSpeed in properties:
            self._moveCalculator.fallSpeed = int(properties[AIPropertyNames.FallSpeed])
        return super().configureProperties(properties)

    def registerOnGroundingHandler(self, callback):
        self._onSpriteHasGrounded = callback

    def calculateMaxFallingTime(self, sprite):
        print("Calculate Falling time.")
        result = None
        offset = sprite.position
        rect = sprite.collideRect
        abort = False
        time = 0
        while not abort:
            time += 8
            y = self._moveCalculator.calcFalling(time)
            position = ViewPoint(offset.left, offset.top + y)
            state = self._collider.checkCollideAt(self._map, rect, position)
            if state.isGrounded:
                result = (time, position)
                abort = True
            elif time > 5000:
                result = (5000, position)
                abort = True

        return result

    def _changeToStandingState(self, sprite, time):
        self._lastChange = None
        self._lastPosition = None
        self._maxMoveTime = None
        sprite.moveState = SpriteMoveState.Standing
        pass

    def _changeToFallingState(self, sprite, time):
        self._lastChange = time
        self._lastPosition = sprite.position
        self._maxMoveTime = self.calculateMaxFallingTime(sprite)
        sprite.moveState = SpriteMoveState.FallingDown
        pass

    def updatePosition(self, sprite, time):
        area = self._collider.checkCollideAt(self._map, sprite.collideRect, sprite.position)
        if sprite.moveState == SpriteMoveState.FallingDown:
            if not self._maxMoveTime:
                self._maxMoveTime = self.calculateMaxFallingTime(sprite)
            
            if time - self._lastChange >= self._maxMoveTime[0]:
                # Maximum falling time reached
                sprite.y = self._maxMoveTime[1].top
                self._changeToStandingState(sprite, time)
                if self._onSpriteHasGrounded:
                    self._onSpriteHasGrounded()
        elif sprite.moveState == SpriteMoveState.Standing:
            if not area.isGrounded:
                self._changeToFallingState(sprite, time)
        else:
            # make shure you are in a defined state.
            sprite.moveState = SpriteMoveState.Standing

        if sprite.moveState == SpriteMoveState.FallingDown:
            duration = time - self._lastChange
            move = self._moveCalculator.calcFalling(duration)
            sprite.y = self._lastPosition.top + move

        return super().updatePosition(sprite, time)


