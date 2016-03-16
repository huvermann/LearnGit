import os.path
import pygame
from Utils.DirHelper import getTMXMapResourceFile
from webcolors import hex_to_rgb
from Utils.ViewPointer import ViewPoint

class TiledLayer():
    """Layer DTO."""
    def __init__(self, config):
        self.data = None
        self.name = None
        self.type = None
        self.width = None
        self.height = None
        self.visible = None
        self.opacity = None
        self._configure(config)
        pass

    def _configure(self, config):
        self.name = config['name']
        self.type = config['type']
        self.width = config['width']
        self.height = config['height']
        self.visible = config['visible']
        self.opacity = config['opacity']
        self.data = config['data']

        pass

class TiledObjectItem():
    def __init__(self, config):
        self.name = None
        self.type = None
        self.x = None
        self.y = None
        self.id = None
        self.gid = None
        self.width = None
        self.height = None
        self.visible = None
        self.properties = None
        self.rotation = None
        self._configure(config)
        pass

    def _configure(self, configure):
        self.name = configure['name']
        self.type = configure['type']
        self.x = int(configure['x'])
        self.y = int(configure['y'])
        self.id = configure['id']
        if 'gid' in configure:
            self.gid = configure['gid']
        self.width = configure['width']
        self.height = configure['height']
        self.visible = configure['visible']
        self.rotation = configure['rotation']
        self.properties = configure['properties']

        pass


class TiledObjectLayer():
    def __init__(self, config):
        self.objects = None
        self.name = None
        self._configure(config)

    def _configure(self, config):
        self.name = config['name']
        self._configureObjectItems(config['objects'])

        pass

    def _configureObjectItems(self, config):
        self.objects = []
        for objConfig in config:
            self.objects.append(TiledObjectItem(objConfig))
        pass

class TiledImageLayer():
    def __init__(self, config, viewName):
        self.__viewName = viewName
        self.name = None
        self.imagePath = None
        self.width = None
        self.height = None
        self.type = None
        self.x = None
        self.y = None
        self._configure(config)
        pass
    
    def _configure(self, config):
        self.name = config['name']
        self.imagePath = config['image']
        self.width = config['width']
        self.height = config['height']
        self.type = config['type']
        self.x = config['x']
        self.y = config['y']
        pass

    def getImageSurface(self):
        result = None
        filename = getTMXMapResourceFile(self.__viewName, self.imagePath)
        if os.path.isfile(filename):
            result = pygame.image.load(filename).convert()
        else:
            raise FileNotFoundError(filename)
        return result



class TileSet():
    '''Tileset DTO'''
    def __init__(self, config, viewName):
        self.columns = None
        self.tilewith = None
        self.tileheight = None
        self.tilecount = None
        self.firstgid = None
        self.imagepath = None
        self.imageheight = None
        self.imagewidth = None
        self.name = None
        self.properties = None
        self.tileproperties = None
        self.transparentcolor = None
        self.surfaceArray = []
        self._configure(config)
        self._loadTileSetImageFile(viewName)
        pass
    def _configure(self, config):
        self.columns = config['columns']
        self.tilewith = config['tilewidth']
        self.tileheight = config['tileheight']
        self.tilecount = config['tilecount']
        self.firstgid = config['firstgid']
        self.imagepath = config['image']
        self.imagewidth = config['imagewidth']
        self.imageheight = config['imageheight']
        self.name = config['name']
        self.properties = config['properties']
        self.transparentcolor = hex_to_rgb(config['transparentcolor'])
        if "tileproperties" in config:
            self.tileproperties = config['tileproperties']

        pass
    def _loadTileSetImageFile(self, viewName):
        filename = getTMXMapResourceFile(viewName, self.imagepath)
        
        if os.path.isfile(filename):
            image = pygame.image.load(filename).convert()
            self.__extractTilesetImages(image)
        else:
            raise FileNotFoundError(filename)

        pass

    def __extractTilesetImages(self, image):
        assert isinstance(image, pygame.Surface), "Image must be of type pygame.Surface"
        countY = self.imageheight // self.tileheight
        countX = self.imagewidth // self.tilewith
        for y in range(0, countY):
            for x in range(0, countX):
                 rect = (x*self.tilewith, y*self.tileheight, self.tilewith, self.tileheight)
                 surface = image.subsurface(rect)
                 if self.transparentcolor:
                     surface.set_colorkey(self.transparentcolor)
                 self.surfaceArray.append(surface)
        pass

class TiledMap(object):
    """Tile map data manager"""
    def __init__(self, jsonConfig, viewName):
        self.__layers = None
        self.__tileSets = None
        self.__imageLayers = None
        self.__map = None
        self._mapTileset = None
        self.__backgroundImage = None
        self.__objects = None
        self.__sprites = None
        self.__player = None
        self.__viewName = viewName
        self.__properties = None
        self.__tileTransparentColor = None
        self.__spaceTiles = None
        self.__ladderTiles = None
        self.configure(jsonConfig, viewName)
        pass

    def configure(self, config, viewName):
        self.__height = config['height']
        self.__width = config['width']
        self.__tileWidth = config['tilewidth']
        self.__tileheight = config['tileheight']
        self.__configureProperties(config['properties'])
        self.__configureLayers(config['layers'], viewName)
        self.configureTileSets(config['tilesets'], viewName)
        self.__map = self.__getMapLayerByName('Map')
        self.__backgroundMap = self.__getMapLayerByName('BackgroundMap')
        self._mapTileset = self.__getTileSetByName('Map')
        self.__backgroundImage = self.__getImageLayerByName('Image')
        try:
            self.__objects = self.__getObjectLayerByName('Objects')
        except SyntaxError:
            print("No objects layer found!")

        self.__sprites = self.__getObjectLayerByName('Sprites')
        self.__player = self.__getPlayerObject()
        self.__tileTransparentColor = self._getTilesetTransparenceColor('Map')
        
        self.__ladderTiles = self.__configureLadderTiles()
        self.__spaceTiles = self.__configureSpaceTiles()

        pass

    def __configureLadderTiles(self):
        result = []
        if self._mapTileset:
            if self._mapTileset.tileproperties:
                for tileNo in self._mapTileset.tileproperties:
                    if 'Ladder' in self._mapTileset.tileproperties[tileNo]:
                        result.append(int(tileNo)+1)
        return result

    def __configureSpaceTiles(self):
        result = [0]
        if self._mapTileset:
            if self._mapTileset.tileproperties:
                for tileNo in self._mapTileset.tileproperties:
                    if 'Space' in self._mapTileset.tileproperties[tileNo]:
                        result.append(int(tileNo)+1)
        #result.extend(self.__ladderTiles)
        return result

                



    def __getMapLayerByName(self, mapName):
        result = None
        liste = list(filter(lambda x: x.name == mapName, self.__layers))
        if liste:
            result = liste[0]
        else:
            raise SyntaxError('Missing Map layer in map file.{0}'.format(mapName))
        return result

    def __getTileSetByName(self, tileSetName):
        result = None
        liste = list(filter(lambda x: x.name == tileSetName, self.__tileSets))
        if liste:
            result = liste[0]
        else:
            raise SyntaxError('Missing tileset: {0}.'.format(tileSetName))
        return result

    def _getTilesetTransparenceColor(self, tileSetName):
        result = None
        tileset = self.__getTileSetByName(tileSetName)
        if tileset:
            result = tileset.transparentcolor
        return result

    def __getImageLayerByName(self, layerName):
        result = None
        liste = list(filter(lambda x: x.name == layerName, self.__imageLayers))
        if liste:
            result = liste[0].getImageSurface()
        else:
            raise SyntaxError("Missing image layer with name 'Image'")
        return result

    
    def __getObjectLayerByName(self, layerName):
        result = None
        liste = list(filter(lambda x: x.name == layerName, self.__objectGroups))
        if liste:
            result = liste[0]
        else:
            raise SyntaxError("Missing object layer with name '{0}'.".format(layerName))
        return result

    def __getPlayerObject(self):
        result = None
        layer = self.__getObjectLayerByName('Player')
        result = layer.objects[0]
        return result


    def __configureProperties(self, config):
        self.__properties = config
        pass
    def __configureLayers(self, config, viewName):
        self.__layers = []
        self.__objectGroups = []
        self.__imageLayers = []
        for layerConfig in config:
            if layerConfig['type']=='tilelayer':
                self.__layers.append(TiledLayer(layerConfig))
            elif layerConfig['type']=='objectgroup':
                self.__objectGroups.append(TiledObjectLayer(layerConfig))
            elif layerConfig['type']=='imagelayer':
                
                self.__imageLayers.append(TiledImageLayer(layerConfig, viewName))
            else:
                t=layerConfig['type']
                raise SyntaxError("Unknown layer type: {0}".format(t))
        pass

    def configureTileSets(self, config, viewName):
        self.__tileSets = []
        for tileSetConfig in config:
            self.__tileSets.append(TileSet(tileSetConfig, viewName))
        pass

    def getTideIndex(self, x, y, layer=None):
        '''Get tide index from map.'''
        xx = x % self.__width
        yy = y % self.__height
        index = yy * self.__width + xx
        if layer == 'BackgroundMap':
            return self.__backgroundMap.data[index]
        else:
            return self.__map.data[index]

    def getTideIndexOnMapCoords(self, mapx, mapy):
        ix = mapx // self.tileWidth
        iy = mapy // self.tileHeight
        return self.getTideIndex(ix, iy)

    def calcTileMapIndex(self, offset, grid, layer=None):
        maxCols =self.width
        maxRows = self.height

        absRow=(offset.top//self.tileHeight+grid[1]) % maxRows
        absCol=(grid[0]+offset.left//self.tileWidth) % maxCols
        return self.getTideIndex(absCol, absRow, layer)

    def calcTileMapXY(self, offset, grid):
        #Todo Only used in plugin ShowTileNumbers
        maxCols =self.width
        maxRows = self.height

        absRow=(offset.top//self.tileHeight+grid[1]) % maxRows
        absCol=(grid[0]+offset.left//self.tileWidth) % maxCols
        return (absCol, absRow)



    def getTileImage(self, index):        
        return self._mapTileset.surfaceArray[index-self._mapTileset.firstgid]


    @property
    def height(self):
        return self.__height
    @property
    def width(self):
        return self.__width

    @property
    def tileWidth(self):
        return self.__tileWidth
    @property
    def tileHeight(self):
        return self.__tileheight

    @property
    def tileTransparentColor(self):
        return self.__tileTransparentColor


    @property
    def backgroundImageSurface(self):
        return self.__backgroundImage

    @property
    def playerConfiguration(self):
        return self.__player

    @property
    def spriteConfiguration(self):
        return self.__sprites

    @property
    def objectsConfiguration(self):
        return self.__objects

    @property
    def spaceTiles(self):
        return self.__spaceTiles

    @property
    def ladderTiles(self):
        return self.__ladderTiles

    @property
    def screenOffset(self):
        result = None
        liste = list(filter(lambda x: x.name == "Screen", self.__objectGroups))
        if liste:
            screenLayer = liste[0]
            screenData = screenLayer.objects[0]
            result = ViewPoint(screenData.x, screenData.y)

        else:
            raise SyntaxError("Missing object layer with name 'Player.")
        return result

    @property
    def properties(self):
        return self.__properties





