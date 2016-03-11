import pygame
import re
from Utils.AnimationInfo import AnimationInfo, MenuAnimationInfo



class MenueItem():
    def __init__(self, resourceName):
        self.id = None
        self.image = None
        self.TargetView = None
        self.action = None
        self.animation = None
        self._resourceName = resourceName
        self._actionObject = None
        

    def configure(self):
        if self.image:
            self.animation = MenuAnimationInfo(self._resourceName, self.image)
    def executeAction(self):
        if self.action:
            actionObject = self.actionFactory(self.action)
            actionObject.doAction()

       

class PlayerMenueSelectorBase(pygame.sprite.Sprite):
    """description of class"""
    def __init__(self):
        self.image = pygame.Surface([32,32])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self._menuItems = []
        self._resourcePath = None
        self._margin = 0
        self._x = None
        self._y = None
        self._imageCreated = None

        super().__init__()

    def configure(self, config):
        self.configureProperties(config.properties)
        self._x = int(config.x)
        # Tiled workaround: fix y-Axis
        self._y = int(config.y - config.height)

        pass

    def configureProperties(self, properties):
        """Configure the menue from tmx properties."""
        for item in properties:
            if item == 'Margin':
                self._margin=  int(properties[item])
            elif item == 'ResourcePath':
                self._resourcePath = properties[item]

        if self._resourcePath:
            for item in properties:
                if item.startswith('MenuItem'):
                    newEntry = self.__parseMenueItemEntry(self._resourcePath, item, properties[item])
                    newEntry.configure()
                    self._menuItems.append(newEntry)

        self._menuItems.sort(key = lambda item: item.id)
        pass

    def __parseMenueItemEntry(self, resourcePath, item, line):
        result = MenueItem(resourcePath)
        result.id =  int(item.replace('MenuItem', ''))
        commands = line.split(' ')
        for cmd in commands:
            parts = cmd.split('=')
            if parts[0] == 'Image':
                result.image = parts[1]
            elif parts[0] == 'TargetView':
                result.TargetView = parts[1]
            elif parts[0] == 'Action':
                result.action == parts[1]

        return result

    def joystickChanged(self, externalInput):
        pass

    def createImage(self):
        result = None
        # Calculate Size
        width = 0
        height = 0
        for item in self._menuItems:
            itemRect = item.animation.ImageRect
            if itemRect.width > width:
                width = itemRect.width
            height += itemRect.height

        # Create transparent surface
        if width == 0:
            widt = 1
        if height == 0:
            height = 1
        result = pygame.Surface([width,height])
        result.fill((1,2,3))
        result.set_colorkey(result.get_at((0,0)))

        # Copy items to surface

        # return the surface
        return result



    def update(self, *args):
        """Updates the image."""
        if not self._imageCreated:
            self.image = self.createImage()
            self._imageCreated = True
        return super().update(*args)



