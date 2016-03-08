from Utils.MapObjectBase import MapObjectBase
from Sprites.LifeLostMessageSprite import LifeLostMessageSprite
from Utils.ServiceLocator import ServiceLocator, ServiceNames

class LifeLostMessage(MapObjectBase):
    """Displays a message if the player is killed."""
    def __init__(self):
        self._screen = ServiceLocator.getGlobalServiceInstance(ServiceNames.Screen)

        return super().__init__()

    def configure(self, configuration):
        #Todo: read the style name from config.
        return super().configure(configuration)

    def initializeObject(self, parent):
        # Register the callback
        parent.lifeLostMessageCallback = self.ShowPlayerHasBeenKilledDialog
        return super().initializeObject(parent)

    def ShowPlayerHasBeenKilledDialog(self, allSprites, objectSprites):
        # Create the Sign-Sprite and adds it to the sprite list.
        dialog = LifeLostMessageSprite()
        dialog.configureFromProperties(self._properties)
        allSprites.add(dialog)
        objectSprites.add(dialog)
        dialog.update()
        pass



