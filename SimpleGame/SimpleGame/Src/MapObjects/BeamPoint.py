from Utils.MapObjectBase import MapObjectBase
from Utils.UserEvents import EVENT_CHANGEVIEW
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.ViewPointer import ViewPoint
import pygame


class BeamPoint(MapObjectBase):
    """Beam points to teleport the player to configured coordinates."""

    def __init__(self):
        """Constructor of the BeamPoint class."""
        super().__init__()
        self._viewName = None
        self._enabled = True

    def initializeObject(self, parent):
        super().initializeObject(parent)
        self._viewName = parent.viewName
        bpReg = ServiceLocator.getGlobalServiceInstance(ServiceNames.BeamPoints)
        bpReg.registerBeamPoint(self)

    def beam(self):
        """Beams the player to this point. Throws a change view event."""
        position = ViewPoint(self._x, self._y)
        event = pygame.event.Event(EVENT_CHANGEVIEW, ViewName = self.viewName, Position = position)
        pygame.event.post(event)

    @property
    def viewName(self):
        return self._viewName

    @property
    def enabled(self):
        return self._enabled

    @property
    def name(self):
        return self._name


