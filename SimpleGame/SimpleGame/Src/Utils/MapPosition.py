class MapPosition(object):
    posX = 0
    posY = 0

    def __init__(self, x, y):
        self.posX = x
        self.posY = y
        pass
    def copy(self):
        return MapPosition(self.posX, self.posY)


