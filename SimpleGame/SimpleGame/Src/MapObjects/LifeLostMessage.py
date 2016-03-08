from Utils.MapObjectBase import MapObjectBase
from Utils.UserEvents import EVENT_NEWGAME
from Sprites.LifeLostMessageSprite import LifeLostMessageSprite
from Utils.ServiceLocator import ServiceLocator, ServiceNames
import pygame

class LifeLostMessage(MapObjectBase):
    """Displays a message if the player is killed."""
    def __init__(self):
        self._screen = ServiceLocator.getGlobalServiceInstance(ServiceNames.Screen)
        self._dialogInitTime = 0
        self._dialogSprite = None

        return super().__init__()

    def configure(self, configuration):
        #Todo: read the style name from config.
        return super().configure(configuration)

    def initializeObject(self, parent):
        # Register the callback
        parent.lifeLostMessageCallback = self.ShowPlayerHasBeenKilledDialog
        
        return super().initializeObject(parent)

    def ShowPlayerHasBeenKilledDialog(self, allSprites, objectSprites):
        self._dialogInitTime = pygame.time.get_ticks()

        # Create the Sign-Sprite and adds it to the sprite list.
        self._dialogSprite = LifeLostMessageSprite()
        self._dialogSprite.configureFromProperties(self._properties)
        allSprites.add(self._dialogSprite)
        objectSprites.add(self._dialogSprite)
        self._dialogSprite.update()
        self._parent.registerEventHandler(self.eventHandler)
        pass

    def closeDialog(self):
        self._parent.unRegisterEventHandler(self.eventHandler)
        self._dialogSprite.kill()
        self._dialogSprite = None
        self._dialogInitTime = 0
        # Raise new game event
        event = pygame.event.Event(EVENT_NEWGAME)
        pygame.event.post(event)
        pass


    def eventHandler(self, events):
        now = pygame.time.get_ticks()
        if now - self._dialogInitTime > 1000:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    self.closeDialog()

                elif event.type == pygame.JOYBUTTONDOWN:
                    self.closeDialog()
        pass



