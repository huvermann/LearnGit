
class MapScanner(object):
    """description of class"""
    def __init__(self, map, sprite):
        self._map = map
        self._sprite = sprite
        self.tileWidth = self._map.tileWidth
        self.tileHeight = self._map.tileHeight


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
        #Todo: Fields benutzen
        sprite = self._sprite
        collideRect = sprite.collideRect
        bottomLeft = collideRect.bottomleft
        bottomRight = collideRect.bottomright
        posLeft = (sprite.x + bottomLeft[0], sprite.y + bottomLeft[1])
        posRight = (sprite.x + bottomRight[0], sprite.y + bottomRight[1])

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
                # Mapende erreicht?
                #if y + 1 + downRows
                downRows += 1
        result = (downRows + 1) * self.tileHeight - yshift -1
        return result

    def scanLeft(self):
        """Returns the number of pixel of space to left."""
        result = 0
        return result

    def scanRight(self):
        """Returns the number of pixel of space to right."""




