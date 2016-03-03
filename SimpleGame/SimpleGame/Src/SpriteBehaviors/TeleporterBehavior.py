from Utils.sprites.SpriteBehaviorBase import SpriteBehaviorBase
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.UserEvents import EVENT_CHANGEVIEW
import pygame

class TeleporterBehavior(SpriteBehaviorBase):
    """Implements a default sprite behavior."""
    def __init__(self, parent, properties):
        self._beamPoint = None
        self._targetViewName = None
        return super().__init__(parent, properties)

    def configureProperties(self, properties):
        #return super().configureProperties(properties)
        if "ViewName" in properties:
            self._targetViewName = properties["ViewName"]
        if "BeamPoint" in properties:
            self._beamPoint = properties["BeamPoint"]


    def doCollide(self):
        """Changes the View and the position."""
        if self._beamPoint:
            print("Beampoint")
            beamService = ServiceLocator.getGlobalServiceInstance(ServiceNames.BeamPoints)
            beamService.beam(self._beamPoint)
        elif self._targetViewName:
            print("ViewTarget")
            event = pygame.event.Event(EVENT_CHANGEVIEW, ViewName = self._targetViewName)
            pygame.event.post(event)
        else:
            raise SyntaxError("Missing Beampoint or ViewName on gate or teleporter object.")

        
        
        pass


