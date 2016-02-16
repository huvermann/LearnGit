from Utils.ViewModelBase2 import ViewModelBase2
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Sprites.SpriteFactory import createSpriteInstance
from Utils.DirHelper import getTMXMapResourceFile
import os.path
import json
from Tiled.TiledMap import TiledMap, TiledObjectLayer
from Tiled.TilesPainter import TilesPainter


class TmxTileMapViewModel(ViewModelBase2):
    """ViewModel for TMX tile maps."""
    def __init__(self, viewName):
        
        super().__init__(viewName)
        self.configureTMX(viewName)
        self._drawTilesCall = TilesPainter.drawTiles
        self._drawBackground = TilesPainter.drawBackground
        ServiceLocator.registerGlobalService(ServiceNames.Map, self.map)
        pass

    def configureTMX(self, viewName):
        """Configure the map data from tmx json file."""
        path = getTMXMapResourceFile(viewName, "map.json")
        configuration = self.loadTMXJson(path)
        self.configureTMXJson(configuration)
        self.player = self.configurePlayer(self.map.playerConfiguration)
        self._viewPointer.screenPosition = self.map.screenOffset
        self.allSprites.add(self.player)
        self.configureSprites(self.map.spriteConfiguration)
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
        self.map = TiledMap(config, self.viewName)
        pass

    def configurePlayer(self, config):
        result = None
        playerClassname = config.type
        result = createSpriteInstance(playerClassname)
        result.configureProperties(config.properties)
        self._viewPointer.playerPosition.left = config.x
        self._viewPointer.playerPosition.top = config.y

        
        return result

    def configureSprites(self, config):
        """Configure the sprite objects for this view."""
        assert isinstance(config, TiledObjectLayer), "Expected config to be TiledObjectLayer."
        assert config.name == "Sprites"
        for sprite in config.objects:
            className = sprite.type
            newSprite = createSpriteInstance(className)
            newSprite.position.left = sprite.x
            newSprite.position.top = sprite.y
            newSprite.configureProperties(sprite.properties)
            self.allSprites.add(newSprite)
            self.objectSprites.add(newSprite)
        pass


