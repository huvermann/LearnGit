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
        self._screenPosition = ViewPoint(0,0)
        self.__playerRect = None
        self.__followStateX = ViewPointerFollowState.FixedPosition
        self.__followStateY = ViewPointerFollowState.FixedPosition

        screen = ServiceLocator.getGlobalServiceInstance(ServiceNames.Screen)
        self.__screenrect = screen.get_rect()
        self._innerBorder = self.__screenrect.copy()
        
        self._innerBorder.left = 40
        self._innerBorder.width -= 80+32
        self._innerBorder.height -= 80+32
        self._innerBorder.top += 40
        #self._innerBorder.right -= 40

        #Center player
        #self.__screenOffset = ViewPoint(self.__screenrect.centerx, self.__screenrect.centery)
        self._playerOffset = ViewPoint(self.__screenrect.centerx, self.__screenrect.centery)
    def mapPositionToScreenOffset(self, position):
        """Converts the abs. map position to screen offset."""
        assert isinstance(position, ViewPoint), "Position must be of type ViewPoint."
        result = None
        left = position.left - self._screenPosition.left
        top = position.top - self._screenPosition.top
        result = ViewPoint(left, top)
        return result

    def getPlayerMapPosition(self):
        return ViewPoint(self.playerPositionX, self.playerPositionY)

    def updateCamera(self):
        """Updates the screen position."""
        if self.__followStateX == ViewPointerFollowState.FixedPosition:
            # Check if right border is reached
            if self._playerOffset.left >= self._innerBorder.right:
                # Safe screen target position
                # Safe time stamp
                # Go into move state
                self.__followStateX = ViewPointerFollowState.FollowLeft
            elif self._playerOffset.left <= self._innerBorder.left:
                # Safe screen target position
                # Safe time stamp
                # Go into move state
                self.__followStateX = ViewPointerFollowState.FollowRight
        if self.__followStateX != ViewPointerFollowState.FixedPosition:
            if self.__followStateX == ViewPointerFollowState.FollowLeft:
                shift = 4
                self._playerOffset.left -= shift
                self._screenPosition.left += shift
                if self._playerOffset.left <= self.__screenrect.centerx:
                    self.__followStateX = ViewPointerFollowState.FixedPosition
            if self.__followStateX == ViewPointerFollowState.FollowRight:
                shift = 4
                self._playerOffset.left += shift
                self._screenPosition.left -= shift
                if self._playerOffset.left>= self.__screenrect.centerx:
                    self.__followStateX = ViewPointerFollowState.FixedPosition

        if self.__followStateY==ViewPointerFollowState.FixedPosition:
            if self._playerOffset.top >= self._innerBorder.bottom:
                self.__followStateY = ViewPointerFollowState.FollowUp
            elif self._playerOffset.top <= self._innerBorder.top:
                self.__followStateY = ViewPointerFollowState.FollowDown

        if self.__followStateY != ViewPointerFollowState.FixedPosition:
            if self.__followStateY == ViewPointerFollowState.FollowUp:
                shift = 4
                self._playerOffset.top -= shift
                self._screenPosition.top += shift
                if self._playerOffset.top <= self.__screenrect.centery:
                    self.__followStateY = ViewPointerFollowState.FixedPosition
            elif self.__followStateY == ViewPointerFollowState.FollowDown:
                shift = 4
                self._playerOffset.top += shift
                self._screenPosition.top -= shift
                if self._playerOffset.top >= self.__screenrect.centery:
                    self.__followStateY = ViewPointerFollowState.FixedPosition

        pass

    @property
    def playerPositionX(self):
        return self._screenPosition.left + self._playerOffset.left
    @playerPositionX.setter
    def playerPositionX(self, value):
        self._playerOffset.left = value - self._screenPosition.left
        pass
    @property
    def playerPositionY(self):
        return self._screenPosition.top + self._playerOffset.top
    @playerPositionY.setter
    def playerPositionY(self, value):
        self._playerOffset.top = value - self._screenPosition.top
        pass

    @property
    def screenPosition(self):
        return self._screenPosition
    #Todo implement setter
    @screenPosition.setter
    def screenPosition(self, value):
        assert isinstance(value, ViewPoint), "screenPosition must be of type ViewPoint."
        self._screenPosition.left = value.left
        self._screenPosition.top = value.top

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
        return self._playerOffset











