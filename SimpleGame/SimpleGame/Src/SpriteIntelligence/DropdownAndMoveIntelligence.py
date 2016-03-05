from Utils.sprites.SpriteBase import SpriteMoveState
from Utils.sprites.SpriteIntelligenceBase import SpriteIntelligenceBase
from SpriteIntelligence import BackAndForthIntelligence, FallDownSpriteIntelligence

class DropdownAndMoveIntelligence(SpriteIntelligenceBase):
    """The sprite first drops down, if it is grounded, it is moving left and right."""
    def __init__(self, parentSprite, properties):
        
        self._dropDown = FallDownSpriteIntelligence.FallDownSpriteIntelligence(parentSprite, properties)
        self._dropDown.registerOnGroundingHandler(self.onSpriteHasGroundedHandler)
        self._isSpriteGrounded = False
        self._moveLeftRight = BackAndForthIntelligence.BackAndForthIntelligence(parentSprite, properties)

        return super().__init__(parentSprite, properties)

    def onSpriteHasGroundedHandler(self):
        self._isSpriteGrounded = True
        pass

    def updatePosition(self, sprite, time):
        if not self._isSpriteGrounded:
            self._dropDown.updatePosition(sprite, time)
        else:
            self._moveLeftRight.updatePosition(sprite, time)
            sprite.intelligence = self._moveLeftRight


