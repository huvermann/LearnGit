from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.ViewPointer import ViewPoint
import pygame

class CheckDirection():
    Ground = 0
    Left = 1
    Right = 2
    Top = 3
    TopLeft = 4
    TopRight = 5

class CollosionSprite(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        super().__init__()
        self.image = image
        self.rect = rect


class TiledWatcher(object):
    """Checks the touched tiles."""
    def __init__(self, parentPlayer):
        """Constructor if the TiledWatcher."""
        print("Constructor: TiledWatcher")
        self.__pyGame = ServiceLocator.getGlobalServiceInstance(ServiceNames.PyGame)
        self.__map = ServiceLocator.getGlobalServiceInstance(ServiceNames.Map)
        self.__player = parentPlayer
        self.__viewPointer = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewPointer)
        self.__spaceTiles = [0,1] # Todo: read this from map
        """Create checkpoint coordinates depending on the player rect."""
        #Todo Implement
        pass

       
    def getTileIndexInMap(self, x, y):
        """Returns the tile map index at map position x,y."""
        return self.__map.getTideIndexOnMapCoords(x, y)

    def isBarrierOnPosition(self, position, direction):
        #Todo: Use real player rect to create the check position.
        result = False
        if direction == CheckDirection.Ground:
            checkx = position.left + 16
            checky = position.top + 32
            tideIndex = self.getTileIndexInMap(checkx, checky)
            return not tideIndex in self.__spaceTiles
        elif direction == CheckDirection.Left:
            #Todo: Implement check
            checkx = position.left + 2
            checky = position.top + 16
            tideIndex = self.getTileIndexInMap(checkx, checky)
            return not tideIndex in self.__spaceTiles
        elif direction == CheckDirection.Right:
            #Todo: Implement check
            checkx = position.left + 30
            checky = position.top + 16
            tideIndex = self.getTileIndexInMap(checkx, checky)
            return not tideIndex in self.__spaceTiles
        elif direction == CheckDirection.Top:
            checkx = position.left + 16
            checky = position.top -6
            tideIndex = self.getTileIndexInMap(checkx, checky)
            return not tideIndex in self.__spaceTiles
        elif direction == CheckDirection.TopLeft:
            checkx = position.left + 2
            checky = position.top -6
            tideIndex = self.getTileIndexInMap(checkx, checky)
            return not tideIndex in self.__spaceTiles
        elif direction == CheckDirection.TopRight:
            checkx = position.left + 30
            checky = position.top -6
            tideIndex = self.getTileIndexInMap(checkx, checky)
            return not tideIndex in self.__spaceTiles

        return result

    def isBarrierOn(self, direction):
        """Checks if there is a barrier in the asked direction."""
        position = ViewPoint(self.__viewPointer.playerPositionX, self.__viewPointer.playerPositionY)
        return self.isBarrierOnPosition(position, direction)


    def standExactOnSurface(self):
        checkx = self.__viewPointer.playerPositionX + 16
        checky = self.__viewPointer.playerPositionY + 31
        tideIndex = self.getTileIndexInMap(checkx, checky)
        res1 = tideIndex in self.__spaceTiles

        checkx = self.__viewPointer.playerPositionX + 16
        checky = self.__viewPointer.playerPositionY + 32
        tideIndex2 = self.getTileIndexInMap(checkx, checky)
        res2 = not tideIndex2 in self.__spaceTiles
        return res1 and res2

    def getBackgroundImage(self, tileMap, offset, sizeRect):
        """Returns an Image of the background at offset with size of sizeRect."""
        result = None
        th = tileMap.tileHeight
        tw = tileMap.tileWidth
        rangex = sizeRect.width//tw
        rangey = sizeRect.height//th
        transparentColor = tileMap.tileTransparentColor

        shiftx = offset.left % tw
        shifty = offset.top % th
        for y in range(0, rangey+1):
            py=y*th-shifty
            for x in range(0, rangex+1):
                bgTileIndex = tileMap.calcTileMapIndex(offset, (x,y))
                if bgTileIndex > 0:
                    if not result:
                        result = self.__pyGame.Surface([sizeRect.width, sizeRect.height])
                        result.set_colorkey(transparentColor)
                        result.fill(transparentColor)
                    tile = tileMap.getTileImage(bgTileIndex)
                    result.blit(tile, (x*tw-shiftx, py))

        return result

    def checkPlayerBackgroundCollosion(self, bgImage, position, sprite):
        """Checks if the bgImage collides with the sprite at the coordinates at the position."""
        result = False
        rect = bgImage.get_rect()
        rect.left = position.left
        rect.top = position.top
        sp = CollosionSprite(bgImage, rect)

        if self.__pyGame.sprite.collide_mask(sprite, sp):
            return True
        return result

    def checkCollosionWithBackground(self, tileMap, position, sprite):
        """Returns true if the sprite collides with the tiled background at position."""
        result = False
        bgImage = self.getBackgroundImage(tileMap, position, sprite.rect)
        if bgImage:
            result = self.checkPlayerBackgroundCollosion(bgImage, position, sprite)
        return result


        







