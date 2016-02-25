from Utils.ViewPluginBase import ViewPluginBase
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Tiled.TiledWatcher import TiledWatcher
from Tiled.TiledMap import TiledMap
import pygame




class CollosionLab(ViewPluginBase):
    """Pluginin to test collosions with background."""
    def __init__(self):
        super().__init__()
        self._player = None
        self._tileCollider = None
        self._map = None
        self._screenRect = None

    def initializePlugin(self, parentView):
        super().initializePlugin(parentView)
        if not self._player:
            self._player = ServiceLocator.getGlobalServiceInstance(ServiceNames.Player)
        self._tileCollider = ServiceLocator.getGlobalServiceInstance(ServiceNames.TiledWatcher)
        self._map = ServiceLocator.getGlobalServiceInstance(ServiceNames.Map)
        self._screenRect = self._screen.get_rect()

    def paintBullet(self, hasCollosion):
        if hasCollosion:
            pygame.draw.circle(self._screen, (255,0,0), (400,400), 8)
        else:
            pygame.draw.circle(self._screen, (0,255,0), (400,400), 8)
        pass

    def drawPlugin(self):
        rect = pygame.Rect(self._screenRect.width - 50, self._screenRect.height -50, 36,36)
        pygame.draw.rect(self._screen, (255,0,0), rect, 1)
        position = self._viewPointer.getPlayerMapPosition()
        bg = self._tileCollider.getBackgroundImage(self._map, position, self._player.rect)
        if bg:
            bgRect = bg.get_rect()
            bgRect.left = rect.left + 2
            bgRect.top = rect.top + 2
            self._screen.blit(bg, bgRect)
            self.paintBullet(self._tileCollider.checkPlayerBackgroundCollosion(bg, position, self._player))
        return super().drawPlugin()



