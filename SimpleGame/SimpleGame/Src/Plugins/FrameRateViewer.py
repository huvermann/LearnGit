from Utils.ViewPluginBase import ViewPluginBase
from Utils.gui.FontProvider import FontProvider
from Utils.ServiceLocator import ServiceLocator, ServiceNames
import pygame

class FrameRateViewer(ViewPluginBase):
    """description of class"""
    def __init__(self):
        gameState = ServiceLocator.getGlobalServiceInstance(ServiceNames.Gamestate)
        self.clock = gameState.clock
        
        super().__init__()
        self._rect = self._screen.get_rect()

    def drawTextLabel(self, x, y, text, font=FontProvider.defaultFont(), color=(0,0,0)):
        label = font.render(text, 1, color)
        textPos = label.get_rect()
        textPos.left = x
        textPos.top = y
        self._screen.blit(label, textPos)
        return textPos

    def drawPlugin(self):
        fps = self.clock.get_fps()
        pos = self.drawTextLabel(10,self._rect.bottom - 20, "FPS: {0:.2f}".format(fps))




