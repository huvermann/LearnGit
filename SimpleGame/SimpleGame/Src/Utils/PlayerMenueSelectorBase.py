import pygame
import re

class MenueItem():
    def __init__(self, **kwargs):
        self.id = None
        self.image = None
        self.TargetView = None
        self.action = None
       

class PlayerMenueSelectorBase(pygame.sprite.Sprite):
    """description of class"""
    def __init__(self):
        self.image = pygame.Surface([32,32])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self._menuItems = []
        self._resourcePath = None
        self._margin = None

        super().__init__()

    def configureProperties(self, properties):
        """Configure the menue from tmx properties."""
        for item in properties:
            if item == 'Margin':
                self._margin=  int(properties[item])
            elif item == 'ResourcePath':
                self._resourcePath = properties[item]
            elif item.startswith('MenuItem'):
                self._menuItems.append(self.parseMenueItemEntry(item, properties[item]))
        pass

    def parseMenueItemEntry(self, item, line):
        result = MenueItem()
        result.id =  int(item.replace('MenuItem', ''))
        commands = line.split(' ')
        for cmd in commands:
            parts = cmd.split('=')
            if 



    def joystickChanged(self, externalInput):
        pass

    def update(self, *args):
        """Updates the image."""
        return super().update(*args)



