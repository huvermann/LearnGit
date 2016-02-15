import pygame
from types import *

class ViewPoint:
    left = 0
    top = 0
    def __init__(self, left, top):
        self.left = left
        self.top = top

class ViewPointer(object):
    """The view pointer keeps the player in the screen"""
    def __init__(self, screenRect, playerRect, innerBorder, posLeft, posTop):
        assert isinstance(screenRect, pygame.Rect), "Expected screenRect to be pygame.Rect."
        assert isinstance(playerRect, pygame.Rect) or playerRect == None, "expected playerRect to be pygame.Rect or None."
        assert isinstance(innerBorder, pygame.Rect) or innerBorder == None, "Expected innerBorder to be pygame.Rect or None."
        assert isinstance(posLeft, int), "Expected leftPos to be integer."
        assert isinstance(posTop, int), "Expected posTop to be integer."
        #assert isinstance(border, pygame.Rect)
        self.__playerPosition = ViewPoint(posLeft, posTop)
        self.__playerRect = playerRect
        self.__screenrect = screenRect
        if not innerBorder:
            self.__innerBorder = self.__screenrect.copy()
            self.__innerBorder.bottom -= 40
            self.__innerBorder.left -= 40
            self.__innerBorder.top += 40
            self.__innerBorder.right -= 40
        else:
            self.__innerBorder = innerBorder

        #Center player
        if self.__playerRect:
            self.__screenOffset = ViewPoint(self.__screenrect.centerx - self.__playerRect.width // 2, self.__screenrect.centery - self.__playerRect.height)
        else:
            self.__screenOffset = ViewPoint(self.__screenrect.centerx, self.__screenrect.centery)

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











