from Utils.MapObjectBase import MapObjectBase, TiledObjectItem
from Utils.ViewModelBase2 import ViewModelBase2
import pygame
from Utils.UserEvents import EVENT_CHANGEVIEW

class PressSpaceOrButtonNavigator(MapObjectBase):
    """Navigates to a view if space or Button is pressed."""
    def __init__(self):
        self._targetViewName = None
        return super().__init__()

    def configure(self, configuration):
        """Gets the target view name."""
        assert isinstance(configuration, TiledObjectItem), "Expected configuration to be of type TiledObjectItem."
        if 'TargetView' in configuration.properties:
            self._targetViewName = configuration.properties['TargetView']
        return super().configure(configuration)

    def initializeObject(self, parent):
        self._parent = parent
        self._parent.registerEventHandler(self.eventHandler)
        return super().initializeObject(parent)

    def eventHandler(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handleKeyboardEvent(event)

            elif event.type == pygame.JOYBUTTONDOWN:
                self.handleJoystickEvent(event)

    def handleKeyboardEvent(self, event):
        if event.key == pygame.K_SPACE:
            self.changeToTargetView()
        pass

    def handleJoystickEvent(self, event):
        self.changeToTargetView()
        pass

    def changeToTargetView(self):
        print("OK, Change to target view.")
        if self._targetViewName:
            changeviewEvent = pygame.event.Event(EVENT_CHANGEVIEW, ViewName=self._targetViewName)
            pygame.event.post(changeviewEvent)

        pass
    


