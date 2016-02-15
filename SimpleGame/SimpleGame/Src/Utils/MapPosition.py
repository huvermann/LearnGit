#Todo: Obsolete remove this class
class MapPosition(object):
    """Map position data transfer object."""
    
    def __init__(self, x, y):
        self._posX = x
        self._posY = y
        pass

    @property
    def posX(self):
        return self._posX
    @posX.setter
    def posX(self, value):
        self._posX = value

    @property
    def posY(self):
        return self._posY
    @posY.setter
    def posY(self, value):
        self._posY = value

    

    def copy(self):
        return MapPosition(self.posX, self.posY)


