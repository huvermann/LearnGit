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
            self.behavior = self.behaviorFactory('DefaultSpriteBehavior')
        if not SpritePropNames.Supplies in properties:
            self.supplies = self.suppliesFactory('Nothing')

        return super().configureFromProperties(properties)

    #def __init__(self):
    #    spritename = SpriteNames.Bloob
    #    super().__init__(spritename)
    #    self._animation = None
    #    self.rect.left = 100
    #    self.loadAnimations()
    #    self._currentAnimation = self._animation[BlobNames.Jump]
    #    self._collosionInfo.sound = SoundNames.BloobTouched
    #    pass

    #def loadAnimationInfo(self, animationName):
    #    result = {}
    #    result["Image"] = SpriteItemBase.loadAnimationFile(self._spriteName, animationName)
    #    result["Count"] = SpriteItemBase.countAnimationLength(result["Image"])
    #    result["ImageSize"] = SpriteItemBase.getPictureSize(result["Image"])
    #    # Set transparence
    #    result["Image"].set_colorkey(result["Image"].get_at((0,0)))
    #    return result

    #def loadAnimations(self):
    #    self._animation = {}
    #    self._animation[BlobNames.Left] = self.loadAnimationInfo(BlobNames.Left)
    #    self._animation[BlobNames.Right] = self.loadAnimationInfo(BlobNames.Right)
    #    self._animation[BlobNames.Die] = self.loadAnimationInfo(BlobNames.Die)
    #    self._animation[BlobNames.Jump] = self.loadAnimationInfo(BlobNames.Jump)

    #def update(self):
    #    """Update the blob sprite."""
    #    rect = SpriteItemBase.getRectTimeBased(self._currentAnimation["Count"], self._currentAnimation["ImageSize"], 100)
    #    self.image = self._currentAnimation["Image"].subsurface(rect)
    #    return super().update()
    #    pass






