from Utils.ViewModelBase2 import ViewModelBase2
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Sprites.SpriteFactory import createSpriteInstance
from Utils.DirHelper import getTMXMapResourceFile
import os.path
import json
from Tiled.TiledMap import TiledMap, TiledObjectLayer
from Tiled.TilesPainter import TilesPainter
from Plugins.PluginFactory import createPluginInstance
from Utils.MapObjectFactory import createObjectInstance
from Utils.sprites.SpriteBase import SpriteBase
from Utils.PlayerMenueSelectorBase import PlayerMenueSelectorBase



class TmxTileMapViewModel(ViewModelBase2):
    """ViewModel for TMX tile maps."""
    def __init__(self, viewName):
        
        super().__init__(viewName)
        self.configureTMX(viewName)
        self._drawTilesCall = TilesPainter.drawTiles
        self._drawBackground = TilesPainter.drawBackground
        pass

    def configureTMX(self, viewName):
        """Configure the map data from tmx json file."""
        path = getTMXMapResourceFile(viewName, "map.json")
        configuration = self.loadTMXJson(path)
        self.configureTMXJson(configuration)
        self._viewPointer.screenPosition = self.map.screenOffset
        self.player = self.configurePlayer(self.map.playerConfiguration)
        self.configurePluginsFromMapProperties(self.map.properties)
        
        self.allSprites.add(self.player)
        if self.map.objectsConfiguration:
            self.configureMapObjects(self.map.objectsConfiguration)
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
        if isinstance(result, PlayerMenueSelectorBase):
            result.configure(config)
        else:
            result.configureProperties(config.properties)
        self._viewPointer.initPlayerPosition(config.x, config.y-config.height)
        return result

    def configureSprites(self, config):
        """Configure the sprite objects for this view."""
        assert isinstance(config, TiledObjectLayer), "Expected config to be TiledObjectLayer."
        assert config.name == "Sprites"
        for sprite in config.objects:
            className = sprite.type
            newSprite = createSpriteInstance(className)
            if not isinstance(newSprite, SpriteBase):
                newSprite.position.left = sprite.x
                newSprite.position.top = sprite.y
                newSprite.configureProperties(sprite.properties)
            else:
                newSprite.configureSprite(sprite)
            self.allSprites.add(newSprite)
            self.objectSprites.add(newSprite)
        pass
    def parseProperty(self, property):
        result = None
        if len(property) == 2:
            propValue = property[1]
            keyValuePair = propValue.split("=")
            if len(keyValuePair) == 2 and keyValuePair[0]=="Plugin":
                result = keyValuePair[1]
        return result



    def configurePluginsFromMapProperties(self, properties):
        """Configures the view plugins from map properties
        this routine searches for a property with a value like:
        Plugin=pluginName
        the Plugin name must be the name of an existing plugin class.
        """
        for prop in properties.items():
            pluginName = self.parseProperty(prop)
            if pluginName:
                instance = createPluginInstance(pluginName)
                if instance:
                    self.plugins.append(instance)
        pass

    def configureMapObjects(self, config):
        assert isinstance(config, TiledObjectLayer), "Expected config to be TiledObjectLayer."
        assert config.name == "Objects", "The layer must have the name 'Objects'."
        
        for obj in config.objects:
            classname = obj.type
            newObject = createObjectInstance(classname)
            newObject.configure(obj)
            self.mapObjects.append(newObject)



