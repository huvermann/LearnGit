from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.ViewPointer import ViewPointer, ViewPoint
from Tiled.TiledSpriteCollider import TiledSpriteCollider, CollisionResult, TileTouchState

class MoveTimeCalculator(object):
    """description of class"""
    def __init__(self, viewPointer, collider, jumpCalculator):
        assert isinstance(viewPointer, ViewPointer), "viewPointer must be of type Utils.ViewPointer.ViewPointer."
        #assert isinstance(tilesWatcher, TiledWatcher), "tilesWatcher must be of type Tiled.TiledWatcher.TiledWatcher."
        assert isinstance(collider, TiledSpriteCollider), "Collider must be of type Tiled.TiledSpriteCollider.TiledSpriteCollider."
        self._viewPointer = viewPointer
        #self._tilesWatcher = tilesWatcher
        self._collider = collider
        self._jumpCalculator = jumpCalculator
        self._map = ServiceLocator.getGlobalServiceInstance(ServiceNames.Map)
        

    def _getOffset(self):
        return ViewPoint(self._viewPointer.playerPositionX, self._viewPointer.playerPositionY)

    def calculateJumpTime(self, vector):
        result = None
        rect = ServiceLocator.getGlobalServiceInstance(ServiceNames.Player).collideRect
        offset = self._getOffset()
        abort = False
        time = 0
        while not abort:
            time += 10
            x = self._jumpCalculator.calcX(time)
            y = self._jumpCalculator.calcY(time)
            position = ViewPoint(offset.left + x * vector.X, offset.top - y)
            state = self._collider.checkCollideAt(self._map, rect, position)
            #if self._tilesWatcher.isBarrierOnPosition(position, CheckDirection.Ground):
            if state.isGrounded or state.isUpperLayerTouched or state.isLeftTouched or state.isRightToched:
                result = (time, position)
                abort = True
            elif time >= 10000:
                result = (10000, position)
                abort = True

        return result

    def calculateMaxJumpUpTime(self):
        result = None
        offset = self._getOffset()
        time = 200
        y = self._jumpCalculator.calcJumpUp(time)
        position = ViewPoint(offset.left, offset.top + y)
        result = (time, position)
        return result


    def calculateMaximumFallDownTime(self):
        result = None
        rect = ServiceLocator.getGlobalServiceInstance(ServiceNames.Player).collideRect
        offset = self._getOffset()
        abort = False
        time = 0
        while not abort:
            time += 10
            y = self._jumpCalculator.calcFalling(time)
            position = ViewPoint(offset.left, offset.top + y)
            state = self._collider.checkCollideAt(self._map, rect, position)
            #if self._tilesWatcher.isBarrierOnPosition(position, CheckDirection.Ground):
            if state.isGrounded:
                result = (time, position)
                abort = True
            elif time >= 10000:
                result = (10000, position)
            
        return result

    def calculateHorizontalMove(self, time):
        return self._jumpCalculator.calcWalking(time, 1)
        


