from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.sprites.SpriteBase import SpriteBase, SpritePropNames



class BloobSprite(SpriteBase):
    """Implementation of the Blob sprite."""
    def configureFromProperties(self, properties):
        # Predefine the coin specific properties
        self.name = 'Bloob'
        self._assetName = 'Bloob'
        self.killPlayer = False
        self.killSprite = True
        self.points = 30
        self.energy = 5
        self.sound = 'beep.wav'
        
        if not SpritePropNames.Style in properties:
            self.style = self.styleFactory('BloobStyle')
        if not SpritePropNames.Intelligence in properties:
            self.intelligence = self.intelligenceFactory('DefaultSpriteIntelligence')
        if not SpritePropNames.Behavior in properties:
            self.behavior = self.behaviorFactory('DefaultSpriteBehavior', properties)
        if not SpritePropNames.Supplies in properties:
            self.supplies = self.suppliesFactory('Nothing')

        return super().configureFromProperties(properties)


       

   




