import pygame
from Utils.DirHelper import getResourceFilePath
import os.path
import json

class TileMapManager:
    """The Tile Map Manager Class."""
    def __init__(self, viewName):
        self._viewName = viewName
        self._position = (0, 0)
        self._mapData = TileMapManager.loadMap(viewName)
        width = self._mapData["tilewidth"]
        height = self._mapData["tileheight"]
        self._tileSet = TileMapManager.loadTileSet(viewName, width, height)
        pass

    def _tileHeight(self):
        return self._mapData["tileheight"]
    def _tileWidth(self):
        return self._mapData["tilewidth"]
    def _viewColumnsCount(self):
        return self._mapData["tileswide"]
    def _viewRowCount(self):
        return self._mapData["tileshigh"]
    tileHeight = property(_tileHeight)
    tileWidth = property(_tileWidth)
    viewColCount = property(_viewColumnsCount)
    viewRowCount = property(_viewRowCount)


    def drawTiles(self, screen, offsetX, offsetY):
        #Todo: Consider offset for index calculation
        rangex, rangey = self.getTileCount(screen)
        for y in range(0,rangey):
            py=y*self.tileHeight
            for x in range(0, rangex):
                px=x*self.tileWidth
                screen.blit(self.calcTile(offsetX, offsetY, x,y), (px, py))
        pass

    def calcTile(self, offsetX, offsetY, column, row):
        """Calculate the tide index and return the correct tileSet."""
        # Todo: Consider offset on index calculation
        index = column + row * self.viewColCount
        layer = self._mapData["layers"][0]["tiles"]
        if len(layer) > index:
            tileIndex = layer[index]["tile"]
        else:
            tileIndex = layer[0]["tile"]
        return self._tileSet[tileIndex][0]

    def getTileCount(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        return (width//self.tileWidth, height//self.tileHeight)

    @staticmethod
    def loadTileSet(viewName, width, height):
        """Loads the tilesets and returns an array of tiles"""
        tileset = None
        filename =getResourceFilePath(viewName + ".png")
        if os.path.isfile(filename):
            image = pygame.image.load(filename).convert()
            image_width, image_height = image.get_size()
            tileset = []
            for tile_x in range(0, image_width//width):
              line = []
              tileset.append(line)
              for tile_y in range(0, image_height//height):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(image.subsurface(rect))
        else:
            raise FileNotFoundError(filename)

        return tileset

    @staticmethod
    def loadMap(mapName):
        """Loads the map from an json file."""
        mapData = None
        mapFileName = getResourceFilePath(mapName + ".map")
        if os.path.isfile(mapFileName):
            with open(mapFileName) as data_file:
                mapData = json.load(data_file)
        else:
            raise FileNotFoundError(mapFileName)
        return mapData


    def _getViewName(self):
        return self._viewName
    viewName = property(_getViewName)

