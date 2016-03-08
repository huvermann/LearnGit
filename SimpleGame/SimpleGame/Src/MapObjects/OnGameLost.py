from Utils.MapObjectBase import MapObjectBase, TiledObjectItem
from Utils.ServiceLocator import ServiceLocator, ServiceNames

class OnGameLost(MapObjectBase):
    """description of class"""
    def __init__(self):
        self._targetViewName = None
        return super().__init__()


    def configure(self, configuration):
        assert isinstance(configuration, TiledObjectItem), "Expected configuration to be of type TiledObjectItem."
        if 'TargetView' in configuration.properties:
            self._targetViewName = configuration.properties['TargetView']
        return super().configure(configuration)

    def initializeObject(self, parent):
        ServiceLocator.registerGlobalService(ServiceNames.GameLostTarget, self._targetViewName)
        return super().initializeObject(parent)

        


