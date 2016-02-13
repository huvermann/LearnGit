from Utils.ViewModelBase2 import ViewModelBase2
from Utils.DirHelper import getTMXMapResourceFile
import os.path
import json
from Tiled.TiledMap import TiledMap


class TmxTileMapViewModel(ViewModelBase2):
    """ViewModel for TMX tile maps."""
    def __init__(self, viewName, screen):
        
        super().__init__(viewName, screen)
        self.configure(viewName)
        pass

    def configure(self, viewName):
        """Configure the map data from tmx json file."""
        path = getTMXMapResourceFile(viewName, "view.map")
        configuration = self.loadTMXJson(path)
        self.configureTMXJson(configuration)
        pass

    def loadTMXJson(self, filename):
        result = None
        if os.path.isfile(filename):
            with open(filename) as data_file:
                result = json.load(data_file)
        else:
            raise FileNotFoundError(filename)
        return result

    def configureTMXJson(self, config):
        self._map = TiledMap(config)
        pass


