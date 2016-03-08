class SavePoint(object):
    """The last saved position of the player and the viewpointer."""
    def __init__(self, **kwargs):
        self._viewName = None
        self._playerPosition = None
        self._screenPosition = None
        if 'viewName' in kwargs:
            self._viewName = kwargs['viewName']
        if 'playerPosition' in kwargs:
            self._playerPosition = kwargs['playerPosition']
        if 'screenPosition' in kwargs:
            self._screenPosition = kwargs['screenPosition']
        pass

    @property
    def viewName(self):
        return self._viewName
    @viewName.setter
    def viewName(self, value):
        self._viewName = value

    @property
    def playerPosition(self):
        return self._playerPosition

    @playerPosition.setter
    def playerPosition(self, value):
        self._playerPosition = value

    @property
    def screenPosition(self):
        return self._screenPosition
    @screenPosition.setter
    def screenPosition(self, value):
        self._screenPosition = value



