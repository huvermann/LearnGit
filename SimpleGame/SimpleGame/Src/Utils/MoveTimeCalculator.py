from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.ViewPointer import ViewPointer, ViewPoint
from Tiled.TiledWatcher import TiledWatcher, CheckDirection

class MoveTimeCalculator(object):
    """description of class"""
    def __init__(self, viewPointer, tilesWatcher, jumpCalculator):
        assert isinstance(viewPointer, ViewPointer), "viewPointer must be of type Utils.ViewPointer.ViewPointer."
        assert isinstance(tilesWatcher, TiledWatcher), "tilesWatcher must be of type Tiled.TiledWatcher.TiledWatcher."
        self._viewPointer = viewPointer
        self._tilesWatcher = tilesWatcher
        self._jumpCalculator = jumpCalculator

    def _getOffset(self):
        return ViewPoint(self._viewPointer.playerPositionX, self._viewPointer.playerPositionY)

    def calculateJumpTime(self, vector):
        result = None
        offset = self._getOffset()
        abort = False
        time = 0
        while not abort:
            time += 10
            x = self._jumpCalculator.calcX(time)
            y = self._jumpCalculator.calcY(time)
            position = ViewPoint(offset.left + x * vector.X, offset.top - y)
            if self._tilesWatcher.isBarrierOnPosition(position, CheckDirection.Ground):
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
        offset = self._getOffset()
        abort = False
        time = 0
        while not abort:
            time += 10
            y = self._jumpCalculator.calcFalling(time)
            position = ViewPoint(offset.left, offset.top + y)
            if self._tilesWatcher.isBarrierOnPosition(position, CheckDirection.Ground):
                result = (time, position)
                abort = True
            elif time >= 10000:
                result = (10000, position)
            
        return result
        


