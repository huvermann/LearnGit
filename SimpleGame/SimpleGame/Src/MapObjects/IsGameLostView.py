from Utils.MapObjectBase import MapObjectBase
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.GameState import GameState

class IsGameLostView(MapObjectBase):
    """Removes all living views from viewController."""
    def initializeObject(self, parent):
        # Destry all view instances
        viewController = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewController)
        viewController.destroyAllRunningViews()
        
        #Reset the game state
        #newGameState = GameState()
        #ServiceLocator.registerGlobalService(ServiceNames.Gamestate, newGameState)
        gameState = ServiceLocator.getGlobalServiceInstance(ServiceNames.Gamestate)
        gameState.reset()
        return super().initializeObject(parent)
    


