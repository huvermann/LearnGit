
class MapScanner(object):
    """description of class"""
    def __init__(self, map, sprite):
        self._map = map
        self._sprite = sprite
        self.tileWidth = self._map.tileWidth
        self.tileHeight = self._map.tileHeight
        self._bottomLeft = None
        self._bottomRight = None
        self._topLeft = None
        self._topRight = None
        

    def initCheckPoints(self):
        collideRect = self._sprite.collideRect
        self._bottomLeft = collideRect.bottomleft
        self._bottomRight = collideRect.bottomright
        self._topLeft = collideRect.topleft
        self._topRight = collideRect.topright

    def getTileAddress(self, position):
        x = position[0] // self.tileWidth
        y = position[1] // self.tileHeight
        return (x, y)

    def isSolidTile(self, index):
        result = False
        if index > 0:
            result = True
            if index in self._map.ladderTiles:
                result = False
            elif index in self._map.spaceTiles:
                result = False
        return result

    def getWayToGround(self):
        """Returns the number of pixel to fall down."""
        result = 0        
        if not self._bottomLeft:
            self.initCheckPoints()
        posLeft = (self._sprite.x + self._bottomLeft[0], self._sprite.y + self._bottomLeft[1])
        posRight = (self._sprite.x + self._bottomRight[0], self._sprite.y + self._bottomRight[1])

        yshift = posLeft[1] % self.tileHeight
        #find the bottom
        bottom = False
        x1, y1 = self.getTileAddress(posLeft)
        x2, y2 = self.getTileAddress(posRight)
        downRows = 0
        while not bottom:
            tide1 = self._map.getTideIndex(x1,y1 +downRows + 1)
            tide2 = self._map.getTideIndex(x2,y2 + downRows + 1)
            if self.isSolidTile(tide1) or self.isSolidTile(tide2):
                bottom = True
            else:
                downRows += 1
        result = (downRows + 1) * self.tileHeight - yshift -1
        return result

    def measureWayToLeft(self):
        """Returns the number of pixel of space to left."""
        result = 0
        posTopLeft = (self._sprite.x + self._topLeft[0], self._sprite.y + self._topLeft[0])
        posBottomLeft = (self._sprite.x + self._bottomLeft[0], self._sprite.y + self._bottomLeft[1])

        xshift = posTopLeft[0] % self.tileWidth
        x1, y1 = self.getTileAddress(posTopLeft)
        x2, y2 = self.getTileAddress(posBottomLeft)
        leftCols = 0
        endOfWay = False
        while not endOfWay:
            upperTide = self._map.getTideIndex(x1 + leftCols - 1, y1)
            lowerTide = self._map.getTideIndex(x2 + leftCols - 1, y1)
            floorTide = self._map.getTideIndex(x2 + leftCols - 1, y2 + 1)
            #if self.isSolidTile
            # Fliesen prüfen, ob weg beendet
            if (self.isSolidTile(upperTide) 
                or self.isSolidTile(lowerTide) 
                or not self.isSolidTile(floorTide)): 
                endOfWay = True
            else:
                leftCols -= 1
        result = (leftCols) * self.tileWidth - xshift
        return result

    def measureWayToRight(self):
        """Returns the number of pixel of space to right."""
        result = 0
        posTopRight = (self._sprite.x + self._topRight[0], self._sprite.y + self._topRight[0])
        posBottomRight = (self._sprite.x + self._bottomRight[0], self._sprite.y + self._bottomRight[1])

        xshift = posTopRight[0] % self.tileWidth

        x1, y1 = self.getTileAddress(posTopRight)
        x2, y2 = self.getTileAddress(posBottomRight)
        rightCols = 0
        endOfWay = False

        while not endOfWay:
            upperTide = self._map.getTideIndex(x1 + rightCols + 1, y1)
            lowerTide = self._map.getTideIndex(x2 + rightCols + 1, y1)
            floorTide = self._map.getTideIndex(x2 + rightCols, y2 + 1)
            #if self.isSolidTile
            # Fliesen prüfen, ob weg beendet
            if (self.isSolidTile(upperTide) 
                or self.isSolidTile(lowerTide) 
                or not self.isSolidTile(floorTide)): 
                endOfWay = True
            else:
                rightCols += 1
        result = (rightCols) * self.tileWidth - xshift - 1
        return result




