from Utils.PlayerBaseClass import PlayerBaseClass
import pygame

class JimboSprite(PlayerBaseClass):
    """Implementation of the Jimbo player behaviour."""
    def __init__(self):
        spriteName = "Jimbo"
        return super().__init__(spriteName)

    def configureProperties(self, properties):
        """Configure special properties."""
        return super().configureProperties(properties)



