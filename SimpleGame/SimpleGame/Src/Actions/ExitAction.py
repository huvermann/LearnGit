from Utils.ActionBaseClass import ActionBaseClass
from Utils.ServiceLocator import ServiceLocator, ServiceNames

class ExitAction(ActionBaseClass):
    """Terminates the game."""
    def doAction(self):
        gamestate = ServiceLocator.getGlobalServiceInstance(ServiceNames.Gamestate)
        gamestate.done = True
        


