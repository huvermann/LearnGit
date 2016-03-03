from Utils.sprites.SpriteBase import SpriteBase, SpritePropNames

class CoinSprite(SpriteBase):
     """A predefined coin sprite class."""
     def configureFromProperties(self, properties):
        # Predefine the coin specific properties
        self.name = 'Coin'
        self._assetName = 'Coin'
        self.killPlayer = False
        self.killSprite = True
        self.points = 30
        self.energy = 5
        self.sound = 'beep.wav'
        
        if not SpritePropNames.Style in properties:
            self.style = self.styleFactory('CoinStyle')
        if not SpritePropNames.Intelligence in properties:
            self.intelligence = self.intelligenceFactory('DefaultSpriteIntelligence')
        if not SpritePropNames.Behavior in properties:
            self.behavior = self.behaviorFactory('DefaultSpriteBehavior')
        if not SpritePropNames.Supplies in properties:
            self.supplies = self.suppliesFactory('Nothing')

        return super().configureFromProperties(properties)





