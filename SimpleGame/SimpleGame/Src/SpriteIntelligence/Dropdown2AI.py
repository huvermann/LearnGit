from Utils.ViewPointer import ViewPoint, ViewPointer
from Utils.sprites.SpriteIntelligenceBase import SpriteIntelligenceBase
from Utils.sprites.SpriteBase import SpriteMoveState
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Tiled.TiledMap import TiledMap
class Dropdown2AI(SpriteIntelligenceBase):
    """description of class"""
    def __init__(self, parentSprite, properties):
        self._map = ServiceLocator.getGlobalServiceInstance(ServiceNames.Map)
        assert isinstance(self._map, TiledMap)

        return super().__init__(parentSprite, properties)

    def updatePosition(self, sprite, time):
        #print(sprite.moveState)
        if not sprite.moveState:
            sprite.moveState = SpriteMoveState.FallingDown
        
        

        return super().updatePosition(sprite, time)


