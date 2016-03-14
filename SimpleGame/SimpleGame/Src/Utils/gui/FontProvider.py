import pygame
from Utils.DirHelper import getFontResourceFile
from Utils.gui.FontProperties import FontProperties

class FontProvider(object):
    """Provides defined fonts"""
    @staticmethod
    def defaultFont():
        return pygame.font.Font(None, 24)

    def smallFont():
        return pygame.font.Font(None, 12)

    @staticmethod
    def getFontByFileName(fontProperties):
        assert isinstance(fontProperties, FontProperties)
        result = None
        sysFontName = None

        if fontProperties.FontName:
            fonts = pygame.font.get_fonts()
            
            if fontProperties.FontName.lower() in fonts:
                sysfontName = fontProperties.FontName
                result = pygame.font.SysFont(sysFontName, fontProperties.Size, False)
            else:
                fname = getFontResourceFile(fontProperties.FontName)
                result = pygame.font.Font(fname, fontProperties.Size)
        else:
            result = pygame.font.Font(fname, fontProperties.Size)
        return result



