import pygame
from types import *
from Utils.ServiceLocator import ServiceLocator, ServiceNames

class ViewPoint:
    left = 0
    top = 0
    def __init__(self, left, top):
        self.left = left
        self.top = top

    def copy(self):
        return ViewPoint(self.left, self.top)


class ViewPointer(object):
    """The view pointer keeps the player in the screen"""
    def __init__(self):
        #assert isinstance(playerRect, pygame.Rect) or playerRect == None, "expected playerRect to be pygame.Rect or None."
        #assert isinstance(innerBorder, pygame.Rect) or innerBorder == None, "Expected innerBorder to be pygame.Rect or None."
        #assert isinstance(posLeft, int), "Expected leftPos to be integer."
        #assert isinstance(posTop, int), "Expected posTop to be integer."
        #self.__playerPosition = ViewPoint(posLeft, posTop)
        #self.__playerRect = playerRect
        self.__playerPosition = ViewPoint(0,0)
        self.__playerRect = None
        screen = ServiceLocator.getGlobalServiceInstance(ServiceNames.Screen)
        self.__screenrect = screen.get_rect()
        self.__innerBorder = self.__screenrect.copy()
        self.__innerBorder.bottom -= 40
        self.__innerBorder.left -= 40
        self.__innerBorder.top += 40
        self.__innerBorder.right -= 40

        #Center player
        self.__screenOffset = ViewPoint(self.__screenrect.centerx, self.__screenrect.centery)

    def changePlayerPosition(self, left, top):
        diffLeft = left - self.__playerPosition.left
        diffTop = top - self.__playerPosition.top
        self.screenOffset.left += diffLeft
        self.screenOffset.top += diffTop
        self.__playerPosition.left = left
        self.__playerPosition.top = top



    def mapPositionToScreenOffset(self, position):
        assert isinstance(position, ViewPoint), "Position must be of type ViewPoint."
        result = None
        absScreenMapPosition = self.screenPosition
        left = position.left - absScreenMapPosition.left
        top = position.top - absScreenMapPosition.top
        result = ViewPoint(left, top)
        return result

    @property
    def playerPosition(self):
        return self.__playerPosition
    @playerPosition.setter
    def playerPosition(self, value):
        assert isinstance(value, ViewPoint), "playerPosition type must be ViewPoint."
        self.__playerPosition = value

    @property
    def screenPosition(self):
        return ViewPoint(self.__playerPosition.left - self.__screenOffset.left, self.__playerPosition.top - self.__screenOffset.top)
    #Todo implement setter
    @screenPosition.setter
    def screenPosition(self, value):
        assert isinstance(value, ViewPoint), "screenPosition must be of type ViewPoint."
        self.__screenOffset.left = self.__playerPosition.left - value.left
        self.__screenOffset.top = self.__playerPosition.top - value.top

    @property
    def playerRect(self):
        return self.__playerRect
    @playerRect.setter
    def playerRect(self, value):
        self.__playerRect = value
        # Center the rect
        self.__screenOffset = ViewPoint(self.__screenrect.centerx - self.__playerRect.width // 2, self.__screenrect.centery - self.__playerRect.height)

    @property
    def screenOffset(self):
        return ViewPoint(self.__playerPosition.left - self.__screenOffset.left, self.__playerPosition.top - self.__screenOffset.top)











