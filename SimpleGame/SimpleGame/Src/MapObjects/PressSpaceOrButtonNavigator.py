from Utils.MapObjectBase import MapObjectBase
from Utils.ViewModelBase2 import ViewModelBase2

class PressSpaceOrButtonNavigator(MapObjectBase):
    """Navigates to a view if space or Button is pressed."""
    def configure(self, configuration):
        return super().configure(configuration)

    def initializeObject(self, parent):
        self._parent.registerEventHandler(self.eventHandler)
        return super().initializeObject(parent)

    def registerEventHandler(self):
        pass
    


