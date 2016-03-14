import pygame
from Utils.gui.FontProvider import FontProvider
import Utils.gui.FontProperties as Gui

class TextLabelSurface(pygame.Surface):
    def __init__(self, text, fontProperties):
        assert isinstance(fontProperties, Gui.FontProperties), "Expected fontPropertys to by of type FontProperties."
        self.text = text
        self._fontProperties = fontProperties
        self.image = None 
        
    def render(self, width=None):
        font = FontProvider.getFontByFileName(self._fontProperties)
        fontImage = font.render(self.text, True, self._fontProperties.Color, self._fontProperties.Background)
        if not width:
            return fontImage
        else:
            rect = fontImage.get_rect()
            self.image = pygame.Surface((width, rect.height))
        
            if self._fontProperties.Background:
                self.image.fill(self._fontProperties.Background)
            else:
                self.image.fill((1,2,3))
                self.image.set_colorkey((1,2,3))
            center = width // 2 - rect.width // 2
            self.image.blit(fontImage, (center, 0))
            return self.image


