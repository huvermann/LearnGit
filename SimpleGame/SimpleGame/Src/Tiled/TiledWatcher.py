from Utils.ServiceLocator import ServiceLocator, ServiceNames

class CheckDirection():
    Ground = 0
    Left = 1
    Right = 2
    Top = 3
    TopLeft = 4
    TopRight = 5


class TiledWatcher(object):
    """Checks the touched tiles."""
    def __init__(self):
        """Constructor if the TiledWatcher."""
        self.__map = ServiceLocator.getGlobalServiceInstance(ServiceNames.Map)
        self.__player = ServiceLocator.getGlobalServiceInstance(ServiceNames.Player)
        self.__viewPointer = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewPointer)
        self.createCheckpoints()
        """Create checkpoint coordinates depending on the player rect."""
        #Todo Implement
        pass
       
    def getTileIndexInMap(x, y):
        """Returns the tile map index at map position x,y."""
        return 0

    def isBarrierOn(self, direction):
        """Checks if there is a barrier in the asked direction."""
        if direction == CheckDirection.Ground:
            #Todo: Implement check
            return True
        elif direction == CheckDirection.Left:
            #Todo: Implement check
            return False
        elif direction == CheckDirection.Right:
            #Todo: Implement check
            return False
        elif direction == CheckDirection.Top:
            #Todo: Implement check
            return False
        elif direction == CheckDirection.TopLeft:
            #Todo: Implement check
            return False
        elif direction == CheckDirection.TopRight:
            #Todo: Implement check
            return False




