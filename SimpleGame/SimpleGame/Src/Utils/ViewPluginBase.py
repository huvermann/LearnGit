import pygame
from Utils.ServiceLocator import ServiceLocator, ServiceNames

class ViewPluginBase(object):
    """The View Plugin base class."""
    def __init__(self):
        self.__enabled = True
        self._screen = ServiceLocator.getGlobalServiceInstance(ServiceNames.Screen)
        self._viewPointer = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewPointer)
        self._curentView = None

    def drawPlugin(self):
        """Draws the plugin."""
        pass

    def update(self):
        """Updates the plugin."""

    def handleEvents(self, events):
        pass


    def registerEventHandler(self):
        # Todo: Implement plugin register mechanism.
        self._curentView = ServiceLocator.getGlobalServiceInstance(ServiceNames.CurrentView)
        if self._curentView:
            self._curentView.registerEventHandler(self.handleEvents)

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, value):
        self.__enabled = value
        


