from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.ViewPointer import ViewPoint

class CheckDirection():
    Ground = 0
    Left = 1
    Right = 2
    Top = 3
    TopLeft = 4
    TopRight = 5


class TiledWatcher(object):
    """Checks the touched tiles."""
    def __init__(self, parentPlayer):
        """Constructor if the TiledWatcher."""
        print("Constructor: TiledWatcher")
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

    def isBarrierOn(self, direction):
        """Checks if there is a barrier in the asked direction."""
        position = ViewPoint(self.__viewPointer.playerPositionX, self.__viewPointer.playerPositionY)

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
            checky = position.top -2
            tideIndex = self.getTileIndexInMap(checkx, checky)
            return not tideIndex in self.__spaceTiles
        elif direction == CheckDirection.TopLeft:
            #Todo: Implement check
            return False
        elif direction == CheckDirection.TopRight:
            #Todo: Implement check
            return False
        #Todo: Implement CanClimbUP /CanClimbDown

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
        







