
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
                if y1 + downRows + 1 >= self._map.height:
                    bottom = True
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
                if x1 + leftCols -1 <= 0:
                    endOfWay = True
        result = leftCols * self.tileWidth + xshift
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
                if x1 + rightCols + 1 >= self._map.width:
                    endOfWay = True
        result = (rightCols) * self.tileWidth + xshift - 1
        return result


    def getWayToNextWallOnRight(self):
        result = 0
        posTopRight = (self._sprite.x + self._topRight[0], self._sprite.y + self._topRight[0])
        posBottomRight = (self._sprite.x + self._bottomRight[0], self._sprite.y + self._bottomRight[1])

        x1, y1 = self.getTileAddress(posTopRight)
        x2, y2 = self.getTileAddress(posBottomRight)
        rightCols = 0
        endOfWay = False
        while not endOfWay:
            upperTile = self._map.getTideIndex(x1 + rightCols, y1)
            lowerTide = self._map.getTideIndex(x2 + rightCols, y2)
            if (self.isSolidTile(upperTile) or self.isSolidTile(lowerTide)):
                endOfWay = True
            else:
                rightCols += 1
                if x1 + rightCols + 1 >= self._map.width:
                    endOfWay = True
        result = rightCols * self.tileWidth
        print("Way to Wall: {0}".format(result))
        return result

    def getWayToNextWallOnLeft(self):
        result = 0
        posTopLeft = (self._sprite.x + self._topLeft[0], self._sprite.y + self._topLeft[0])
        posBottomLeft = (self._sprite.x + self._bottomLeft[0], self._sprite.y + self._bottomLeft[1])
        xshift = posTopLeft[0] % self.tileWidth

        x1, y1 = self.getTileAddress(posTopLeft)
        x2, y2 = self.getTileAddress(posBottomLeft)

        leftCols = 0
        endOfWay = False
        while not endOfWay:
            upperTile = self._map.getTideIndex(x1 + leftCols, y1)
            lowerTide = self._map.getTideIndex(x2 + leftCols, y2)
            if (self.isSolidTile(upperTile) or self.isSolidTile(lowerTide)):
                endOfWay = True
            else:
                leftCols -= 1
                if x1 + leftCols -1 <= 0:
                    endOfWay = True
                    
        result = leftCols * self.tileWidth + 16
        print("Way to left Wall: {0}".format(result)) 

        return result

    #def calculateJumpTime(self, vector):
    #    result = 0
    #    calculator = self._sprite.moveCalculator
    #    left = self._sprite.x
    #    top = self._sprite.y
    #    endOfWay = False
    #    while not endOfWay:
    #        time += 10
    #        x = calculator.calcX(time) * vector + left
    #        y = calculator.calcY(time) + top
    #        if vector == 1:
    #            posTop = (self._sprite.x + self._topRight[0], self._sprite.y + self._topRight[0])
    #            posBottom = (self._sprite.x + self._bottomRight[0], self._sprite.y + self._bottomRight[1])
    #        else:
    #            posTop = (left + self._topLeft[0], top + self._topLeft[0])
    #            posBottom = (left + self._bottomLeft[0], top + self._bottomLeft[1])

    #        x1, y1 = self.getTileAddress(posTop)
    #        x2, y2 = self.getTileAddress(posBottom)
    #        upperTile = self._map.getTideIndex(x1, y1)
    #        lowerTile = self._map.getTileIndex(x2, y2)





            
        return result



