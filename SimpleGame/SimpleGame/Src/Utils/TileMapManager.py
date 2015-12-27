import pygame
from Views.DirHelper import getResourceFilePath
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

    def drawTiles(self, screen):
        i = 0
        for tile in self._tileSet:
            #print(tile)
            screen.blit(tile[0], (30, 16*i))
            i+=1
        pass

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

