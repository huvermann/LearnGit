import pygame
from Utils.DirHelper import getMapImageResourceFile, getMapResourceFile, getBackgroundImageResourceFile
import os.path
import json
from Utils.Constants import MapFields, Corners

class TileMapManager:
    """The Tile Map Manager Class."""
    def __init__(self, viewName):
        self._viewName = viewName
        self._position = (0, 0)
        self._mapData = TileMapManager.loadMap(viewName)
        self._backgroundImage = TileMapManager.loadBackgroundImage(viewName)
        self._tileMapArray = TileMapManager.getTileMapArray(self._mapData)
        width = self._mapData[MapFields.Tilewidth]
        height = self._mapData[MapFields.Tileheight]
        self._tileSet = TileMapManager.loadTileSet(viewName, width, height, transparence=(self.loadBackgroundImage != None))
        self._tileSetWith = len(self._tileSet)
        self._tileSetHeight = len(self._tileSet[0])
        pass

    def _tileHeight(self):
        
        return self._mapData[MapFields.Tileheight]
    def _tileWidth(self):
        return self._mapData[MapFields.Tilewidth]
    def _viewColumnsCount(self):
        return self._mapData[MapFields.Tileswide]
    def _viewRowCount(self):
        return self._mapData[MapFields.Tileshigh]
    tileHeight = property(_tileHeight)
    tileWidth = property(_tileWidth)
    viewColCount = property(_viewColumnsCount)
    viewRowCount = property(_viewRowCount)

    def _drawBackground(self, screen, image):
        screen.blit(image, (0,0))
        pass

    def drawTiles(self, screen, offset):
        if self._backgroundImage:
            self._drawBackground(screen, self._backgroundImage)

        th = self.tileHeight
        tw = self.tileWidth

        shiftx = offset[0] % tw
        shifty = offset[1] % th
        rangex, rangey = self.getTileCount(screen)
        for y in range(0,rangey+2):
            py=y*th-shifty
            for x in range(0, rangex+2):
                tileIndex=self.calcTileMapIndex(offset, (x,y))
                if (tileIndex > 0) or (self._backgroundImage == None):
                    # Draw all tiles except index 0
                    screen.blit(self.calcTile(offset, (x,y)), (x*tw-shiftx, py))
        pass

    def calcTile(self, offset, grid):
        """Calculate the tide index and return the correct tileSet."""
        tileIndex = self.calcTileMapIndex(offset, grid)
        return self.getTileMapImage(tileIndex)

    def calcTileMapIndex(self, offset, grid):
        maxCols =self._mapData[MapFields.Tileswide]
        maxRows = self._mapData[MapFields.Tileshigh]

        absRow=(offset[1]//self.tileHeight+grid[1]) % maxRows
        absCol=(grid[0]+offset[0]//self.tileWidth) % maxCols
        return self._tileMapArray[absRow][absCol]

    def getTileMapImage(self, tileIndex):
        ix = tileIndex % self._tileSetWith
        iy = tileIndex // self._tileSetWith
        try:
            result = self._tileSet[ix][iy]
        except IndexError:
            print("Index error! TileIndex:{} IX: {}. IY: {}".format(tileIndex, ix, iy))
            result = self._tileSet[0][0]
        return result

    def getTileCount(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        return (width//self.tileWidth, height//self.tileHeight)

    @staticmethod
    def getTouchedTileOf(position, mapData, tileMap, tileDimension):
        col = (position[0] // tileDimension[0]) % mapData[MapFields.Tileswide]
        row = (position[1] // tileDimension[1]) % mapData[MapFields.Tileshigh]
        #index = self.getTileType(col, row)
        index = tileMap[row][col]
        return {"col": col, "row": row, "index": index}


    def getTouchedTiles(self, playerPosition, spriteDimensions):
        """Retuns the tiles that the sprite touches at the offset position."""
        
        #topLeft = playerPosition
        topRight = (playerPosition[0]+spriteDimensions[0], playerPosition[1])
        bottomLeft = (playerPosition[0], playerPosition[1]+spriteDimensions[1])
        bottomRight = (playerPosition[0] + spriteDimensions[0], playerPosition[1] + spriteDimensions[1])
        groundContact = (playerPosition[0] + spriteDimensions[0] // 2, playerPosition[1] + spriteDimensions[1] + 2)

        tileDim = (self.tileWidth, self.tileHeight)
        touched = {}
        touched[Corners.TopLeft] = TileMapManager.getTouchedTileOf(playerPosition, self._mapData, self._tileMapArray, tileDim)
        touched[Corners.TopRight] = TileMapManager.getTouchedTileOf(topRight, self._mapData, self._tileMapArray, tileDim)
        touched[Corners.BottomLeft] = TileMapManager.getTouchedTileOf(bottomLeft, self._mapData, self._tileMapArray, tileDim)
        touched[Corners.BottomRight] = TileMapManager.getTouchedTileOf(bottomRight, self._mapData, self._tileMapArray, tileDim)
        touched[Corners.GroundContact] = TileMapManager.getTouchedTileOf(groundContact, self._mapData, self._tileMapArray, tileDim)
       
        return touched

    def getPlayerTileCoordinate(self, screen, offset):
        """Kachel-Koordinate des spielers berechnen."""
        rangeX, rangeY = self.getTileCount(screen)
        centerGrid = (rangeX // 2, rangeY // 2)
        maxCols =self._mapData[MapFields.Tileswide]
        maxRows = self._mapData[MapFields.Tileshigh]

        absRow=((offset[1]//self.tileHeight+centerGrid[1]) % maxRows)+1
        absCol=((centerGrid[0]+offset[0]//self.tileWidth) % maxCols)
        return (absCol, absRow)

    def getTileType(self, col, row):
        return self._tileMapArray[row][col]


    @staticmethod
    def loadBackgroundImage(viewName):
        image = None
        filename = getBackgroundImageResourceFile(viewName)
        if os.path.isfile(filename):
            image = pygame.image.load(filename).convert()
        return image

    @staticmethod
    def loadTileSet(viewName, width, height, transparence = False):
        """Loads the tilesets and returns an array of tiles"""
        tileset = None
        filename =getMapImageResourceFile(viewName)
        if os.path.isfile(filename):
            image = pygame.image.load(filename).convert()
            image_width, image_height = image.get_size()
            transparencColor = image.get_at((0,0)) # get the transparence color
            tileset = []
            for tile_x in range(0, image_width//width):
              line = []
              tileset.append(line)
              for tile_y in range(0, image_height//height):
                rect = (tile_x*width, tile_y*height, width, height)
                img = image.subsurface(rect)
                if transparence:
                    img.set_colorkey(transparencColor)
                line.append(img)
        else:
            raise FileNotFoundError(filename)

        return tileset

    @staticmethod
    def loadMap(mapName):
        """Loads the map from an json file."""
        mapData = None
        mapArray = None
        mapFileName = getMapResourceFile(mapName)
        if os.path.isfile(mapFileName):
            with open(mapFileName) as data_file:
                mapData = json.load(data_file)
        else:
            raise FileNotFoundError(mapFileName)
        return mapData

    @staticmethod
    def getTileMapArray(mapData):
        cols = mapData[MapFields.Tileswide]
        rows = mapData[MapFields.Tileshigh]
        layer = mapData[MapFields.Layers][0][MapFields.Tiles]
        result = []
        for y in range(rows):
            line=[0]*cols
            for x in range(cols):
                index = x + y * cols
                line[x]=layer[index][MapFields.Tile]
            result.append(line)
        return result


    def _getViewName(self):
        return self._viewName
    viewName = property(_getViewName)

