import pygame
from Utils.SpriteItemBase import SpriteItemBase
from Sprites.MagicSpriteStrings import SpriteNames
from Utils.Constants import SoundNames
from Utils.ServiceLocator import ServiceLocator, ServiceNames

class CoinSprite(SpriteItemBase):
    """Implementation of the coin sprite."""
    def __init__(self):
        resourceName = SpriteNames.Coin
        super().__init__(resourceName)
        self._animation = None
        self.loadAnimations(resourceName)
        self._collosionInfo.sound = SoundNames.CoinTouched
        pass

    def configureProperties(self, properties):
        super().configureProperties(properties)
        # Check to configured properties here.
        pass

    def update(self):
        # calculate position
        rect = SpriteItemBase.getRectTimeBased(self._animation["Count"], self._animation["ImageSize"], 100)
        self.image = self._animation["Image"].subsurface(rect)
        #self.rect.left, self.rect.top = self._calcScreenPositionCallback(self._position)
        return super().update()

   
    def loadAnimations(self, spriteName):
        self._animation = {}
        self._animation["Image"]= SpriteItemBase.loadAnimationFile(spriteName, "Ani")
        if self._animation["Image"]:
            self._animation["Image"].set_colorkey(self._animation["Image"].get_at((0,0)))
            self._animation["Count"] = SpriteItemBase.countAnimationLength(self._animation["Image"])
            self._animation["ImageSize"] = SpriteItemBase.getPictureSize(self._animation["Image"])





