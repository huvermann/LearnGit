class CollosionInfo(object):
    """The colosion info data object."""
    def __init__(self, spriteDies = True, playerDies = False, points = 10, parent = None, sound=None, metaData = None):
        """Initializes the collosion info DTO."""
        self._spriteDies = spriteDies
        self._playerDies = playerDies
        self._points = points
        self._parent = parent
        self._sound = sound
        self._metaData = metaData
        pass

    @property
    def spriteDies(self):
        return self._spriteDies
    @spriteDies.setter
    def spriteDies(self, value):
        self._spriteDies = value
    @property
    def playerDies(self):
        return self._playerDies
    @playerDies.setter
    def playerDies(self, value):
        self._playerDies = value

    @property
    def points(self):
        return self._points
    @points.setter
    def points(self, value):
        self._points = value

    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def metaData(self):
        return self._metaData
    @metaData.setter
    def metaData(self, value):
        self._metaData = value

    @property
    def sound(self):
        return self._sound
    @sound.setter
    def sound(self, value):
        self._sound = value


