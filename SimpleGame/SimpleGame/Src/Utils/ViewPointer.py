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

class ViewPointerFollowState:
    FixedPosition = 0
    FollowRight = 1
    FollowLeft = 2
    FollowUp = 3
    FollowDown = 4
    


class ViewPointer(object):
    """The view pointer keeps the player in the screen"""
    def __init__(self):
        #Screen Position in map
        self.__screenPosition = ViewPoint(0,0)
        self.__playerRect = None
        self.__followStateX = ViewPointerFollowState.FixedPosition
        self.__followStateY = ViewPointerFollowState.FixedPosition

        screen = ServiceLocator.getGlobalServiceInstance(ServiceNames.Screen)
        self.__screenrect = screen.get_rect()
        self.__innerBorder = self.__screenrect.copy()
        self.__innerBorder.bottom -= 40
        self.__innerBorder.left = 40
        self.__innerBorder.width -= 40
        self.__innerBorder.top += 40
        self.__innerBorder.right -= 40

        #Center player
        #self.__screenOffset = ViewPoint(self.__screenrect.centerx, self.__screenrect.centery)
        self.__playerOffset = ViewPoint(self.__screenrect.centerx, self.__screenrect.centery)
    def mapPositionToScreenOffset(self, position):
        """Converts the abs. map position to screen offset."""
        assert isinstance(position, ViewPoint), "Position must be of type ViewPoint."
        result = None
        left = position.left - self.__screenPosition.left
        top = position.top - self.__screenPosition.top
        result = ViewPoint(left, top)
        return result

    def getPlayerMapPosition(self):
        return ViewPoint(self.playerPositionX, self.playerPositionY)

    def updateCamera(self):
        """Updates the screen position."""
        if self.__followStateX == ViewPointerFollowState.FixedPosition:
            # Check if right border is reached
            if self.__playerOffset.left >= self.__innerBorder.right:
                # Safe screen target position
                # Safe time stamp
                # Go into move state
                self.__followStateX = ViewPointerFollowState.FollowLeft
            elif self.__playerOffset.left <= self.__innerBorder.left:
                # Safe screen target position
                # Safe time stamp
                # Go into move state
                self.__followStateX = ViewPointerFollowState.FollowRight
        if self.__followStateX != ViewPointerFollowState.FixedPosition:
            if self.__followStateX == ViewPointerFollowState.FollowLeft:
                shift = 4
                self.__playerOffset.left -= shift
                self.__screenPosition.left += shift
                if self.__playerOffset.left <= self.__screenrect.centerx:
                    self.__followStateX = ViewPointerFollowState.FixedPosition
            if self.__followStateX == ViewPointerFollowState.FollowRight:
                shift = 4
                self.__playerOffset.left += shift
                self.__screenPosition.left -= shift
                if self.__playerOffset.left>= self.__screenrect.centerx:
                    self.__followStateX = ViewPointerFollowState.FixedPosition

        if self.__followStateY==ViewPointerFollowState.FixedPosition:
            if self.__playerOffset.top >= self.__innerBorder.bottom:
                self.__followStateY = ViewPointerFollowState.FollowUp
            elif self.__playerOffset.top <= self.__innerBorder.top:
                self.__followStateY = ViewPointerFollowState.FollowDown

        if self.__followStateY != ViewPointerFollowState.FixedPosition:
            if self.__followStateY == ViewPointerFollowState.FollowUp:
                shif = 4
                self.__playerOffset.top -= shift
                self.__screenPosition.top += shift
                if self.__playerOffset.top <= self.__screenrect.centery:
                    self.__followStateY = ViewPointerFollowState.FixedPosition
            elif self.__followStateY == ViewPointerFollowState.FollowDown:
                shift = 4
                self.__playerOffset.top += shift
                self.__screenPosition.top -= shift
                if self.__playerOffset.top >= self.__screenrect.centery:
                    self.__followStateY = ViewPointerFollowState.FixedPosition

        pass





    #@property
    #def playerPosition(self):
    #    return ViewPoint(self.__screenPosition.left + self.__playerOffset.left,
    #                     self.__screenPosition.top + self.__playerOffset.top)
    #@playerPosition.setter
    #def playerPosition(self, value):
    #    assert isinstance(value, ViewPoint), "playerPosition type must be ViewPoint."
    #    self.__playerOffset.left = self.__screenPosition.left - value.left
    #    self.__playerOffset.top = self.__screenPosition.top - value.top

    @property
    def playerPositionX(self):
        return self.__screenPosition.left + self.__playerOffset.left
    @playerPositionX.setter
    def playerPositionX(self, value):
        self.__playerOffset.left = value - self.__screenPosition.left
        pass
    @property
    def playerPositionY(self):
        return self.__screenPosition.top + self.__playerOffset.top
    @playerPositionY.setter
    def playerPositionY(self, value):
        self.__playerOffset.top = value - self.__screenPosition.top
        pass

    @property
    def screenPosition(self):
        return self.__screenPosition
    #Todo implement setter
    @screenPosition.setter
    def screenPosition(self, value):
        assert isinstance(value, ViewPoint), "screenPosition must be of type ViewPoint."
        self.__screenPosition.left = value.left
        self.__screenPosition.top = value.top

    #@property
    #def playerRect(self):
    #    return self.__playerRect
    #@playerRect.setter
    #def playerRect(self, value):
    #    self.__playerRect = value
    #    # Center the rect
    #    self.__screenOffset = ViewPoint(self.__screenrect.centerx - self.__playerRect.width // 2, self.__screenrect.centery - self.__playerRect.height)

    @property
    def playerOffset(self):
        return self.__playerOffset

    @property
    def screenOffset(self):
        return self.__screenPosition











