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

        self._cameraSpeed = 20

        screen = ServiceLocator.getGlobalServiceInstance(ServiceNames.Screen)
        self._screenrect = screen.get_rect()
        self.__innerBorder = self._screenrect.copy()
        
        self.__innerBorder.left = 80
        self.__innerBorder.width -= 160+32
        self.__innerBorder.height -= 160+32
        self.__innerBorder.top += 80

        self.__mapHeight = None
        self.__mapWidth = None

        #Center player
        self._playerOffset = ViewPoint(self._screenrect.centerx, self._screenrect.centery)
    def mapPositionToScreenOffset(self, position):
        """Converts the abs. map position to screen offset."""
        assert isinstance(position, ViewPoint), "Position must be of type ViewPoint."
        result = None
        left = position.left - self._screenPosition.left
        top = position.top - self._screenPosition.top
        result = ViewPoint(left, top)
        return result

    def centerPlayerPositionToScreen(self, playerPosition):
        """Move the player to that position and centers the player on the screen."""
        assert isinstance(playerPosition, ViewPoint), "Expected playerPosition to be of type ViewPoint."
        if playerPosition.left - self._screenrect.centerx > 0:
            self.screenPosition.left = playerPosition.left - self._screenrect.centerx
            self._playerOffset.left = self._screenrect.centerx
            #Todo: protect the viewPointer to place the screen behind the right border of the map.
        else:
            self.screenPosition.left = 0
            self._playerOffset.left = playerPosition.left

        if playerPosition.top - self._screenrect.centery > 0:
            self.screenPosition.top = playerPosition.top - self._screenrect.centery
            self._playerOffset.top = self._screenrect.centery
            #Todo: Protect the viewPointer to place the screen behind the lower border of the map.
        else:
            self.screenPosition.top = 0
            self._playerOffset.top = playerPosition.top
        
        
        pass

    def getPlayerMapPosition(self):
        return ViewPoint(self.playerPositionX, self.playerPositionY)

    def updateCamera(self):
        """Updates the screen position."""
        if self.__followStateX == ViewPointerFollowState.FixedPosition:
            # Check if right border is reached
            if self._playerOffset.left >= self.__innerBorder.right:
                if self.screenPosition.left < self.mapWidth - self._screenrect.width:
                    self.__followStateX = ViewPointerFollowState.FollowLeft

            elif self._playerOffset.left <= self.__innerBorder.left:
                if self._screenPosition.left > self.__innerBorder.left:
                    self.__followStateX = ViewPointerFollowState.FollowRight

        if self.__followStateX != ViewPointerFollowState.FixedPosition:
            if self.__followStateX == ViewPointerFollowState.FollowLeft:
                self._playerOffset.left -= self._cameraSpeed
                self._screenPosition.left += self._cameraSpeed
                if self._playerOffset.left <= self._screenrect.centerx:
                    self.__followStateX = ViewPointerFollowState.FixedPosition
                if self.screenPosition.left >= self.mapWidth - self._screenrect.width:
                    self.__followStateX = ViewPointerFollowState.FixedPosition

            if self.__followStateX == ViewPointerFollowState.FollowRight:
                self._playerOffset.left += self._cameraSpeed
                self._screenPosition.left -= self._cameraSpeed
                if self._playerOffset.left>= self._screenrect.centerx:
                    self.__followStateX = ViewPointerFollowState.FixedPosition

        if self.__followStateY==ViewPointerFollowState.FixedPosition:
            if self._playerOffset.top >= self.__innerBorder.bottom:
                self.__followStateY = ViewPointerFollowState.FollowUp
            elif self._playerOffset.top <= self.__innerBorder.top:
                self.__followStateY = ViewPointerFollowState.FollowDown

        if self.__followStateY != ViewPointerFollowState.FixedPosition:
            if self.__followStateY == ViewPointerFollowState.FollowUp:
                self._playerOffset.top -= self._cameraSpeed
                self._screenPosition.top += self._cameraSpeed
                # Check player goes out of screen
                if self._playerOffset.top > self._screenrect.bottom - self.__innerBorder.left:
                    diff = 50
                    self._playerOffset.top -= diff
                    self._screenPosition.top += diff

                if self._playerOffset.top <= self._screenrect.centery:
                    self.__followStateY = ViewPointerFollowState.FixedPosition
            elif self.__followStateY == ViewPointerFollowState.FollowDown:
                self._playerOffset.top += self._cameraSpeed
                self._screenPosition.top -= self._cameraSpeed
                if self._playerOffset.top >= self._screenrect.centery:
                    self.__followStateY = ViewPointerFollowState.FixedPosition

        pass

    def initPlayerPosition(self, x, y):
        """Initialize the player position."""
        self._playerOffset.left = x - self._screenPosition.left
        self._playerOffset.top = y - self._screenPosition.top
        pass

    @property
    def playerPositionX(self):
        return self._screenPosition.left + self._playerOffset.left
    @playerPositionX.setter
    def playerPositionX(self, value):
        if value > self.__innerBorder.left:
            if value < self.__mapWidth - self.__innerBorder.left:
                self._playerOffset.left = value - self._screenPosition.left
        pass
    @property
    def playerPositionY(self):
        return self._screenPosition.top + self._playerOffset.top
    @playerPositionY.setter
    def playerPositionY(self, value):
        if value > self.__innerBorder.top:
            if value < self.__mapHeight - self.__innerBorder.top:
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

    @property
    def mapHeight(self):
        return self.__mapHeight

    @mapHeight.setter
    def mapHeight(self, value):
        self.__mapHeight = value

    @property
    def mapWidth(self):
        return self.__mapWidth

    @mapWidth.setter
    def mapWidth(self, value):
        self.__mapWidth = value

    @property
    def playerOffset(self):
        return self._playerOffset











