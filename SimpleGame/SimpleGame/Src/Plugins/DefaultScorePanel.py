from Utils.ViewPluginBase import ViewPluginBase
from Utils.gui.FontProvider import FontProvider

class DefaultScorePanel(ViewPluginBase):
    """Plugin to draw the ScorePanel."""
    def __init__(self):
        super().__init__()
        self._screenRect = self._screen.get_rect()
        self._fontColor = (0,0,0)


    def drawTextLabel(self, x, y, text, font=FontProvider.defaultFont(), color=(0,0,0)):
        label = font.render(text, 1, color)
        textPos = label.get_rect()
        textPos.left = x
        textPos.top = y
        self._screen.blit(label, textPos)
        pass

    def drawFrame(self):
        pass

    def drawLives(self):
        pass

    def drawPoints(self):
        self.drawTextLabel(10, 10, "Points: {0}".format(100))
        pass

    def drawEnergy(self):
        pass



    def drawPlugin(self):
        self.drawFrame()
        self.drawLives()
        self.drawPoints()
        self.drawEnergy()
        return super().drawPlugin()
