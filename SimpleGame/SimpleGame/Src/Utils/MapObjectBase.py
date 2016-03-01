from Tiled.TiledMap import TiledObjectItem
#from Utils.ViewModelBase2 import ViewModelBase2

class MapObjectBase(object):
    """The map object base class."""
    def __init__(self):
        self._parent = None
        self._name = None
        self._properties = None
        self._x = None
        self._y = None
        self._width = None
        self._height = None
        

    def configure(self, configuration):
        """Configure the object from tmx object layer configuration."""
        assert isinstance(configuration, TiledObjectItem), "Expected config to be TiledObjectItem."

        self._name = configuration.name
        self._x = configuration.x
        self._y = configuration.y
        self._width = configuration.width
        self._height = configuration.height
        self._properties = configuration.properties
        pass

    def initializeObject(self, parent):
        #assert isinstance(parent, ViewModelBase2), "Expected parent to be of type ViewModelBase2."
        self._parent = parent



