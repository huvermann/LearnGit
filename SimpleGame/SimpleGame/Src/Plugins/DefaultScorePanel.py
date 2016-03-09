from Utils.ViewPluginBase import ViewPluginBase
from Utils.gui.FontProvider import FontProvider
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.GameState import GameState

class DefaultScorePanel(ViewPluginBase):
    """Plugin to draw the ScorePanel."""
    def __init__(self):
        super().__init__()
        self._screenRect = self._screen.get_rect()
        self._fontColor = (0,0,0)
        self._status = ServiceLocator.getGlobalServiceInstance(ServiceNames.Gamestate)
        assert isinstance(self._status, GameState)


    def drawTextLabel(self, x, y, text, font=FontProvider.defaultFont(), color=(0,0,0)):
        label = font.render(text, 1, color)
        textPos = label.get_rect()
        textPos.left = x
        textPos.top = y
        self._screen.blit(label, textPos)
        return textPos

    def drawPlugin(self):
        pos = self.drawTextLabel(10, 10, "Points: {0}".format(self._status.points))
        pos = self.drawTextLabel(10, pos.bottom + 8, "Energy: {0}".format(self._status.energy))
        pos = self.drawTextLabel(10, pos.bottom + 8, "Lifes: {0}".format(self._status.lifes))

        pos = self.drawTextLabel(9, 9, "Points: {0}".format(self._status.points), color = (255,255,255))
        pos = self.drawTextLabel(9, pos.bottom + 8, "Energy: {0}".format(self._status.energy), color = (255,255,255))
        pos = self.drawTextLabel(9, pos.bottom + 8, "Lifes: {0}".format(self._status.lifes), color = (255,255,255))
        #return super().drawPlugin()
