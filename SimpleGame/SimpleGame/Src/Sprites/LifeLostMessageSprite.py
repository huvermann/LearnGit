from Utils.sprites.SpriteBase import SpriteBase, SpritePropNames

class LifeLostMessageSprite(SpriteBase):
    """Displays a player lost life message"""
    def configureFromProperties(self, properties):
        # Predefine the coin specific properties
        self.name = 'LifeLostMessage'
        self._assetName = 'LifeLostMessage'
        self.killPlayer = False
        self.killSprite = False
        self.points = 0
        self.energy = 0
        self.sound = None
        
        if not SpritePropNames.Style in properties:
            self.style = self.styleFactory('LifeLostMessageStyle', properties)
        if not SpritePropNames.Intelligence in properties:
            self.intelligence = self.intelligenceFactory('CenterOnScreenIntelligence', properties)
        if not SpritePropNames.Behavior in properties:
            self.behavior = self.behaviorFactory('DefaultSpriteBehavior', properties)
        if not SpritePropNames.Supplies in properties:
            self.supplies = self.suppliesFactory('Nothing', properties)

        return super().configureFromProperties(properties)


