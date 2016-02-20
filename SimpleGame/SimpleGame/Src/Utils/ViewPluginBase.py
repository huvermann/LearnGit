import pygame
from Utils.ServiceLocator import ServiceLocator, ServiceNames

class ViewPluginBase(object):
    """The View Plugin base class."""
    def __init__(self):
        self.__enabled = True
        self._screen = ServiceLocator.getGlobalServiceInstance(ServiceNames.Screen)
        self._viewPointer = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewPointer)

    def drawPlugin(self):
        """Draws the plugin."""
        pass

    def update(self):
        """Updates the plugin."""

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, value):
        self.__enabled = value
        


