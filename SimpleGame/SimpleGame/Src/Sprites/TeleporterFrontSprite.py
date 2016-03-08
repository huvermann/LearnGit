class TeleporterFrontSprite(object):
    """description of class"""
from Utils.sprites.SpriteBase import SpriteBase, SpritePropNames
#from Utils.UserEvents import EVENT_CHANGEVIEW

class TeleporterFrontSprite(SpriteBase):
    """description of class"""
    def configureFromProperties(self, properties):
        self.name = 'Tele'
        self._assetName = 'Teleporter'
        self.killPlayer = False
        self.killSprite = False
        self.points = 0
        self.energy = 0
        self.sound = None
        
        if not SpritePropNames.Style in properties:
            self.style = self.styleFactory('TeleporterFrontStyle', properties)
        if not SpritePropNames.Intelligence in properties:
            self.intelligence = self.intelligenceFactory('DefaultSpriteIntelligence', properties)
        if not SpritePropNames.Behavior in properties:
            self.behavior = self.behaviorFactory('DefaultSpriteBehavior', properties)
        if not SpritePropNames.Supplies in properties:
            self.supplies = self.suppliesFactory('Nothing', properties)

        return super().configureFromProperties(properties)


