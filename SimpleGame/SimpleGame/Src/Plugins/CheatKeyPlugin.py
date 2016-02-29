from Utils.ViewPluginBase import ViewPluginBase
from Utils.ServiceLocator import ServiceLocator, ServiceNames
import Utils.UserEvents
import Utils.ViewPointer
import pygame

class CheatKeyPlugin(ViewPluginBase):
    """Plugin to hook keystrokes only for development use."""
    def __init__(self):
        return super().__init__()

    def initializePlugin(self, parentView):
        super().initializePlugin(parentView)
        self.registerEventHandler()

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handleKeyboardEvent(event)

    def handleKeyboardEvent(self, event):
        if event.key == pygame.K_t:
            # On 't' change to Training Level.
            changeviewEvent = pygame.event.Event(Utils.UserEvents.EVENT_CHANGEVIEW, ViewName='Training', Position=Utils.ViewPointer.ViewPoint(89, 206))
            pygame.event.post(changeviewEvent)
        elif event.key == pygame.K_F1:
            changeviewEvent = pygame.event.Event(Utils.UserEvents.EVENT_CHANGEVIEW, ViewName='Level1')
            pygame.event.post(changeviewEvent)
        elif event.key == pygame.K_F2:
            changeviewEvent = pygame.event.Event(Utils.UserEvents.EVENT_CHANGEVIEW, ViewName='Level2')
            pygame.event.post(changeviewEvent)
        elif event.key == pygame.K_F3:
            changeviewEvent = pygame.event.Event(Utils.UserEvents.EVENT_CHANGEVIEW, ViewName='Level3')
            pygame.event.post(changeviewEvent)





