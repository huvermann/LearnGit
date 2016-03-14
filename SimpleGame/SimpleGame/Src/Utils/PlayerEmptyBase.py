import pygame
class PlayerEmptyBase(pygame.sprite.Sprite):
    """description of class"""
    def __init__(self, *groups):
        self.image = pygame.Surface([2,2])
        self.image.fill((0,0,0))
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.rect = self.image.get_rect()

        return super().__init__(*groups)

    def configureProperties(self, properties):
        pass

    def joystickChanged(self, joystick):
        pass



