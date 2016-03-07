import pygame

class FontProvider(object):
    """Provides defined fonts"""
    @staticmethod
    def defaultFont():
        return pygame.font.Font(None, 24)

    def smallFont():
        return pygame.font.Font(None, 12)


