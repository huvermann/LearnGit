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

class TileSet():
    '''Tileset DTO'''
    def __init__(self, config):
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
        self._configure(config)
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
        if "tileproperties" in config:
            self.tileproperties = config['tileproperties']

        pass

class TiledMap(object):
    """Tile map data manager"""
    def __init__(self, jsonConfig):
        self._layers = None
        self._tileSets = None
        self.configure(jsonConfig)
        pass

    def configure(self, config):
        self._height = config['height']
        self._width = config['width']
        self._tileWidth = config['tilewidth']
        self._tileheight = config['tileheight']
        self._configureProperties(config['properties'])
        self._configureLayers(config['layers'])
        self.configureTileSets(config['tilesets'])
        self._prepareMainLayerMap()
        pass

    def _prepareMainLayerMap(self):
        liste = list(filter(lambda x: x.name == 'Map', self._layers))
        if liste:
            self._map = liste[0]
        else:
            raise SyntaxError('Missing Map layer in map file.')
        pass


    def _configureProperties(self, config):
        pass
    def _configureLayers(self, config):
        self._layers = []
        for layerConfig in config:
            self._layers.append(TiledLayer(layerConfig))
        pass

    def configureTileSets(self, config):
        self._tileSets = []
        for tileSetConfig in config:
            self._tileSets.append(TileSet(tileSetConfig))
        pass

    def getTideIndex(self, x, y):
        '''Get tide index from map.'''
        idx = y * self._width + x
        return self._map[idx]




