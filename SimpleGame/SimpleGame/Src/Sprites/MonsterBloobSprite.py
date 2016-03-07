from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.sprites.SpriteBase import SpriteBase, SpritePropNames



class MonsterBloobSprite(SpriteBase):
    """Implementation of the Blob sprite."""
    def configureFromProperties(self, properties):
        # Predefine the coin specific properties
        self.name = 'Monster_Bloob'
        self._assetName = 'Monster_Bloob'
        self.killPlayer = True
        self.killSprite = False
        self.points = 0
        self.energy = 0
        self.sound = 'Beep'
        
        if not SpritePropNames.Style in properties:
            self.style = self.styleFactory('MonsterBloobStyle', properties)
        if not SpritePropNames.Intelligence in properties:
            self.intelligence = self.intelligenceFactory('DropdownAndMoveIntelligence', properties)
        if not SpritePropNames.Behavior in properties:
            self.behavior = self.behaviorFactory('DefaultSpriteBehavior', properties)
        if not SpritePropNames.Supplies in properties:
            self.supplies = self.suppliesFactory('Nothing', properties)

        return super().configureFromProperties(properties)