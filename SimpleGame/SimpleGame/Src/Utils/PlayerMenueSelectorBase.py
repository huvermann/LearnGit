import pygame

class PlayerMenueSelectorBase(pygame.sprite.Sprite):
    """description of class"""
    def __init__(self):
        self.image = pygame.Surface([32,32])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        super().__init__()

    def configureProperties(self, properties):
        """Configure the menue from tmx properties."""
        print(properties)
        pass

    def joystickChanged(self, externalInput):
        pass

    def update(self, *args):
        """Updates the image."""
        return super().update(*args)



