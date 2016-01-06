from Utils.PlayerBaseClass import PlayerBaseClass
import pygame

class JimboSprite(PlayerBaseClass):
    """Implementation of the Jimbo player behaviour."""
    def __init__(self, screen):
        spriteName = "Jimbo"
        return super().__init__(screen, spriteName)



