import pygame
from Utils.SpriteItemBase import SpriteItemBase
from Sprites.MagicSpriteStrings import SpriteNames

class BlobSprite(SpriteItemBase):
    """Implementation of the Blob sprite."""
    def __init__(self, screen, position):
        spritename = SpriteNames.Blob
        super().__init__(screen, spritename, position)
        self._animation = None
        pass



