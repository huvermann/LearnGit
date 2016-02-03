import pygame
from Utils.SpriteItemBase import SpriteItemBase
from Sprites.MagicSpriteStrings import SpriteNames

class CoinSprite(SpriteItemBase):
    """Implementation of the coin sprite."""
    def __init__(self, screen, position):
        spritename = SpriteNames.Coin
        super().__init__(screen, spritename, position)
        self._animation = None
        pass

    def loadAnimations(self, spriteName):
        self._animation = SpriteItemBase.loadAnimationFile(spriteName, "")
        if self._animation:
            self._transparenceKey = self._animation.get_at((0,0))
            self._animation.set_colorkey(self._transparenceKey)


