from Utils.ViewPluginBase import ViewPluginBase
from Utils.gui.FontProvider import FontProvider
import pygame

class FrameRateViewer(ViewPluginBase):
    """description of class"""

    def drawTextLabel(self, x, y, text, font=FontProvider.defaultFont(), color=(0,0,0)):
        label = font.render(text, 1, color)
        textPos = label.get_rect()
        textPos.left = x
        textPos.top = y
        self._screen.blit(label, textPos)
        return textPos

    def drawPlugin(self):
        fps = pygame.time.Clock.get_fps()
        pos = self.drawTextLabel(10,10, "FPS: {0}".format(fps))        
        #return super().drawPlugin()




