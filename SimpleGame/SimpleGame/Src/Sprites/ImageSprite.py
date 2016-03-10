
from Utils.sprites.SpriteBase import SpriteBase, SpritePropNames

class ImageSprite (SpriteBase):
     """A predefined generic image sprite class."""
     def configureFromProperties(self, properties):
        # Predefine the image specific properties
        self.name = 'Images'
        self._assetName = 'Images'
        self.killPlayer = False
        self.killSprite = False
        self.points = 0
        self.energy = 0
        self.sound = None
        
        if not SpritePropNames.Style in properties:
            self.style = self.styleFactory('ImageStyle', properties)
        if not SpritePropNames.Intelligence in properties:
            self.intelligence = self.intelligenceFactory('DefaultSpriteIntelligence', properties)
        if not SpritePropNames.Behavior in properties:
            self.behavior = self.behaviorFactory('DefaultSpriteBehavior', properties)
        if not SpritePropNames.Supplies in properties:
            self.supplies = self.suppliesFactory('Nothing', properties)

        return super().configureFromProperties(properties)

