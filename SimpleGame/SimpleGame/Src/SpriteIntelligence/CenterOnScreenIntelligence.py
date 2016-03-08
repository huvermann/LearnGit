from Utils.sprites.SpriteIntelligenceBase import SpriteIntelligenceBase
from Utils.ServiceLocator import ServiceLocator, ServiceNames

class CenterOnScreenIntelligence(SpriteIntelligenceBase):
    """Centers the sprite on the screen."""
    def __init__(self, parentSprite, properties):
        self._screen = ServiceLocator.getGlobalServiceInstance(ServiceNames.Screen)

        return super().__init__(parentSprite, properties)

    def updatePosition(self, sprite, time):
        screenRect = self._screen.get_rect()
        width = sprite.rect.width
        height = sprite.rect.height
        sprite.rect.left = screenRect.centerx-width // 2
        sprite.rect.top = screenRect.centery - height // 2

        #return super().updatePosition(sprite, time)


