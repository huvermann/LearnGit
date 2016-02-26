import pygame
from Utils.SpriteItemBase import SpriteItemBase
from Sprites.MagicSpriteStrings import SpriteNames
from Utils.Constants import SoundNames
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.UserEvents import EVENT_CHANGEVIEW

class DrawbridgeSprite(SpriteItemBase):
    """description of class"""
    def __init__(self):
        resourceName = SpriteNames.Drawbridge
        super().__init__(resourceName)
        self._animation = None
        self.loadAnimations(resourceName)
        self._collosionInfo.sound = SoundNames.CoinTouched
        self._collosionInfo.spriteDies = False
        self._viewTargetName = None
        
        pass

    def doCollide(self):
        if self._viewTargetName:
            # Change the view
            event = pygame.event.Event(EVENT_CHANGEVIEW, ViewName = self._viewTargetName)
            pygame.event.post(event)
        return super().doCollide()

    def configureProperties(self, properties):
        super().configureProperties(properties)
        # Check to configured properties here.
        if "ViewName" in properties:
            self._viewTargetName = properties["ViewName"]
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



