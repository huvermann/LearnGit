from Utils.ViewPointer import ViewPoint, ViewPointer
from Utils.sprites.SpriteIntelligenceBase import SpriteIntelligenceBase
from Utils.sprites.SpriteBase import SpriteMoveState
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Tiled.TiledMap import TiledMap
from Tiled.MapScanner import MapScanner

class MoveTargetPosition():
    x = None
    y = None
    time = None
    def __init__(self, time, x, y):
        self.time = time
        self.x = x
        self.y = y


class Dropdown2AI(SpriteIntelligenceBase):
    """description of class"""
    def __init__(self, parentSprite, properties):
        self._map = ServiceLocator.getGlobalServiceInstance(ServiceNames.Map)
        assert isinstance(self._map, TiledMap)
        self._mapScanner = MapScanner(self._map, parentSprite)
        self._targetPosition = None
        self._lastPosition = None
        self._lastTime = None
        self._walkspeed = None
        self._fallSpeed = 0.2

        return super().__init__(parentSprite, properties)

    def savePosition(self, sprite, time):
        self._lastPosition = (sprite.x, sprite.y)
        self._lastTime = time
        pass

    def updateMoveState(self, sprite, time):
        if sprite.moveState == SpriteMoveState.Standing:
            self.checkStanding(sprite, time)
        elif sprite.moveState == SpriteMoveState.FallingDown:
            self.checkFallingDown(sprite, time)
        elif sprite.moveState in [SpriteMoveState.MoveLeft, SpriteMoveState.MoveRight]:
            self.checkMoving(sprite, time)
        pass



    def checkStanding(self, sprite, time):
        level = self._mapScanner.getWayToGround()
        if level > 0:
            self.changeToFalling(sprite, time)
        pass

    def checkFallingDown(self, sprite, time):
        # Position über Zeit berechnen
        level = self._mapScanner.getWayToGround()
        if level == 0:
            self.changeToStanding(sprite, time)
        if time >= self._targetPosition.time:
            self.changeToStanding(sprite, time)
        pass
    def checkMoving(self, sprite, time):
        level = self._mapScanner.getWayToGround()
        if level > 0:
            self.changeToFalling(sprite, time)
        pass

    def changeToFalling(self, sprite, time):
        def calculateBounce(sprite, time):
            
            down = int(self._mapScanner.getWayToGround())
            falltime = int(down // self._fallSpeed)
            return MoveTargetPosition(falltime + time, sprite.x, sprite.y + down)

        #Save the starting position
        self.savePosition(sprite, time)
        self._targetPosition = calculateBounce(sprite, time)

        sprite.moveState = SpriteMoveState.FallingDown
        pass

    def changeToStanding(self, sprite, time):
        if self._targetPosition:
            sprite.x = self._targetPosition.x
            sprite.y = self._targetPosition.y
            self._targetPosition = None

        self._lastPosition = None
        self._lastTime = None
        sprite.moveState = SpriteMoveState.Standing
        pass

    def calculateFallingPosition(self, sprite, time):
        """Sprite is falling, calculate the position."""
        if not self._lastTime:
            self.savePosition(sprite, time)
        down = (time - self._lastTime) * self._fallSpeed
        sprite.y = int(self._lastPosition[1] + down)
        
        pass

    def calculateMovePosition(self, sprite, time):
        """Sprite is moving, calculate the position."""
        pass


    def calculateNewPosition(self, sprite, time):
        if sprite.moveState == SpriteMoveState.FallingDown:
            #Calculate position
            self.calculateFallingPosition(sprite, time)
        elif sprite.moveState in [SpriteMoveState.MoveLeft, SpriteMoveState.MoveRight]:
            self.calculateMovePosition(sprite, time)
       
        pass

    def updatePosition(self, sprite, time):
        if not sprite.moveState:
            sprite.moveState = SpriteMoveState.Standing
        self.updateMoveState(sprite, time)
        self.calculateNewPosition(sprite, time)
        
        

        return super().updatePosition(sprite, time)


