from Utils.MapObjectBase import MapObjectBase
from Utils.ViewModelBase2 import ViewModelBase2


class IsLevelSavePoint(MapObjectBase):
    """Register the save point on initialization of the view."""

    def initializeObject(self, parent):
        assert isinstance(parent, ViewModelBase2)
        parent.registerSavePoint()
        return super().initializeObject(parent)


