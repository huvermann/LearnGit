import pygame
from Utils.SpriteItemBase import SpriteItemBase
from Sprites.MagicSpriteStrings import SpriteNames
from Utils.Constants import SoundNames

class DrawbridgeSprite(SpriteItemBase):
    """description of class"""
    def __init__(self, position, calcScreenPositionCallback):
        resourceName = SpriteNames.Drawbridge
        super().__init__(resourceName, position, calcScreenPositionCallback)
        self._animation = None
        self.loadAnimations(resourceName)
        self._collosionInfo.sound = SoundNames.CoinTouched
        pass

    def update(self):
        # calculate position
        rect = SpriteItemBase.getRectTimeBased(self._animation["Count"], self._animation["ImageSize"], 100)
        self.image = self._animation["Image"].subsurface(rect)
        self.rect.left, self.rect.top = self._calcScreenPositionCallback(self._position)
        pass

    def loadAnimations(self, spriteName):
        self._animation = {}
        self._animation["Image"]= SpriteItemBase.loadAnimationFile(spriteName, "Ani")
        if self._animation["Image"]:
            self._animation["Image"].set_colorkey(self._animation["Image"].get_at((0,0)))
            self._animation["Count"] = SpriteItemBase.countAnimationLength(self._animation["Image"])
            self._animation["ImageSize"] = SpriteItemBase.getPictureSize(self._animation["Image"])


