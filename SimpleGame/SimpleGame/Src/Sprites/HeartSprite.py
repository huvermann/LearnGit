from Utils.sprites.SpriteBase import SpriteBase, SpritePropNames

class HeartSprite(SpriteBase):
    """A bumping heart sprite."""
    def configureFromProperties(self, properties):
        # Predefine the coin specific properties
        self.name = 'Heart'
        self._assetName = 'Heart'
        self.killPlayer = False
        self.killSprite = True
        self.points = 30
        self.energy = 5
        self.sound = 'beep.wav'
        
        if not SpritePropNames.Style in properties:
            self.style = self.styleFactory('HeartStyle', properties)
        if not SpritePropNames.Intelligence in properties:
            self.intelligence = self.intelligenceFactory('DefaultSpriteIntelligence', properties)
        if not SpritePropNames.Behavior in properties:
            self.behavior = self.behaviorFactory('DefaultSpriteBehavior', properties)
        if not SpritePropNames.Supplies in properties:
            self.supplies = self.suppliesFactory('Nothing', properties)

        return super().configureFromProperties(properties)



