import pygame

class ViewModelBase2():
    """Viewmodel base class."""

    def __init__(self, viewName, screen):
        """Constructor of the ViewModel base class."""
        self._viewName = viewName
        self._screen = screen
        self._map = None
        self._tileColider = None
        self._player = None
        self._objectSprites = pygame.sprite.Group()
        self._allSprites = pygame.sprite.Group()

    @property
    def screen(self):
        return self._screen
    @screen.setter
    def screen(self, value):
        self._screen = value

    @property
    def viewName(self):
        return self._viewName
    @viewName.setter
    def viewName(self, value):
        self._viewName = value

    @property
    def map(self):
        return self._map

    @property
    def player(self):
        return self._player
    @player.setter
    def player(self, value):
        self._player = value

    @property
    def objectSprites(self):
        return self._objectSprites

    @property
    def allSprites(self):
        return self._allSprites

    def runView(self):
        """Runs the view."""
        pass


