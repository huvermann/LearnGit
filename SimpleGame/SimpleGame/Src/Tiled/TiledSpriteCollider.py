from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Tiled.TiledMap import TiledMap
from Utils.ViewPointer import ViewPoint


class TileTouchState():
    Space = 1
    DockLeft = 2 # The point is on the edge of a til
    DockRight = 3
    DockUp = 4
    DockDown = 5
    InsideLeft = 6
    InsideRight = 7
    InsideUp = 8
    InsideDown = 9

class CollisionDetail():
    TideIndex = None
    State = None
    StateVertical = None
    StateHorizontal = None
    VerticalShift= None
    HorizontalShift = None
    MataData = None

class CheckPoints():
        TopLeft = None
        TopRight = None
        Center = None
        BottomLeft = None
        BottomRight = None
        Left = None
        Right = None

class CollisionResult(object):
    def __init__(self, map, rect, position):
        self._map = map
        self._rect = rect
        self._position = position
        self._checkPoints = self._prepareCheckpoints()
        self._MiddleHorizontal = map.tileHeight // 2
        self._middleVertical = map.tileWidth // 2
        self.TopLeft = self.__touchAt(self._checkPoints.TopLeft)
        self.TopRight = self.__touchAt(self._checkPoints.TopRight)
        self.Center = self.__touchAt(self._checkPoints.Center)
        self.BottomLeft = self.__touchAt(self._checkPoints.BottomLeft)
        self.BottomRight = self.__touchAt(self._checkPoints.BottomRight)
        self.Left = self.__touchAt(self._checkPoints.Left)
        self.Right = self.__touchAt(self._checkPoints.Right)

    def _prepareCheckpoints(self):
        result = CheckPoints()

        result.TopLeft = ViewPoint(self._rect.left + self._position.left, self._rect.top + self._position.top - 1)
        result.TopRight = ViewPoint(self._rect.left + self._position.left + self._rect.width, self._rect.top + self._position.top - 1)
        result.BottomLeft = ViewPoint(self._rect.left + self._position.left + 1, self._rect.top + self._position.top + self._rect.height)
        result.BottomRight = ViewPoint(self._rect.left + self._position.left + self._rect.width - 1, self._rect.top + self._position.top + self._rect.height)
        result.Center = ViewPoint(self._rect.left + self._position.left + self._rect.width // 2, self._rect.top + self._position.top + self._rect.height // 2)
        result.Left = ViewPoint(self._rect.left + self._position.left, self._position.top + self._rect.top + self._rect.height //2)
        result.Right = ViewPoint(self._rect.left + self._position.left + self._rect.width, self._rect.top + self._position.top + self._rect.height // 2)

        return result

    def __touchAt(self, touchPoint):
        result = CollisionDetail()
        result.TideIndex = self._map.getTideIndexOnMapCoords(touchPoint.left, touchPoint.top)


        if result.TideIndex in self._map.spaceTiles:
            result.State = TileTouchState.Space
        else:
            # calculate if tile is on an edge
            result.HorizontalShift =  touchPoint.left % self._map.tileWidth
            result.VerticalShift = touchPoint.top % self._map.tileHeight
            if result.VerticalShift == 0:
                result.StateVertical = TileTouchState.DockDown
            elif result.VerticalShift == self._map.tileHeight - 1:
                result.StateVertical = TileTouchState.DockUp
            
            elif result.VerticalShift > self._middleVertical:
                result.StateVertical = TileTouchState.InsideUp
            else:
                result.StateVertical = TileTouchState.InsideDown

            if result.HorizontalShift == 0:
                result.StateHorizontal = TileTouchState.DockLeft
            elif result.HorizontalShift == self._map.tileWidth - 1:
                result.StateHorizontal = TileTouchState.DockRight
            elif result.HorizontalShift > self._MiddleHorizontal:
                result.StateHorizontal = TileTouchState.InsideRight
            else:
                result.StateHorizontal = TileTouchState.InsideLeft
                
        return result


    @property
    def isGrounded(self):
        result = self.BottomLeft.State != TileTouchState.Space or self.BottomRight.State != TileTouchState.Space
        return result

    @property
    def isStandOnSurface(self):
        if self.BottomLeft.State != TileTouchState.Space:
            if self.BottomLeft.VerticalShift:
                return self.BottomLeft.VerticalShift < 5
            if self.BottomRight.VerticalShift:
                return self.BottomRight.VerticalShift < 5
        return False

    @property
    def isDockGround(self):
        result = self.isGrounded and (self.BottomLeft.StateVertical == TileTouchState.DockDown or self.BottomRight.StateVertical == TileTouchState.DockDown)
        return result

    @property
    def isLeftTouched(self):
        result = (self.Left.StateHorizontal == TileTouchState.DockLeft 
                  or self.Left.StateHorizontal == TileTouchState.InsideRight) and self.Left.TideIndex not in self._map.ladderTiles
        return result
    
    @property
    def isRightToched(self):
        result = (self.Right.StateHorizontal == TileTouchState.InsideLeft
                  or self.Right.StateHorizontal == TileTouchState.DockRight) and self.Right.TideIndex not in self._map.ladderTiles
        return result

    @property
    def isLeftDocked(self):
        result = (self.Left.StateHorizontal == TileTouchState.DockLeft)
        return result

    @property
    def isRightDocked(self):
        result = (self.Right.StateHorizontal == TileTouchState.DockRight)
        return result

    @property
    def isUpperLayerTouched(self):
        result = (self.TopLeft.StateVertical == TileTouchState.InsideUp
                  or self.TopRight.StateVertical == TileTouchState.InsideUp 
                  or self.TopLeft.StateVertical == TileTouchState.DockUp 
                  or self.TopRight.StateVertical == TileTouchState.DockUp)
        return result

    @property
    def isUpperLayerDocked(self):
        result = (self.TopLeft.StateVertical == TileTouchState.DockUp
                  or self.TopRight.StateVertical == TileTouchState.DockUp)
        return result

    @property
    def isLadderTouched(self):
        result = (self.BottomLeft.TideIndex in self._map.ladderTiles 
                  or self.BottomRight.TideIndex in self._map.ladderTiles
                  or self.Center.TideIndex in self._map.ladderTiles)
        return result

    @property
    def isLadderOnFeeds(self):
        result = (self.BottomLeft.TideIndex in self._map.ladderTiles 
                  or self.BottomRight.TideIndex in self._map.ladderTiles)
        return result

    @property
    def isStandingOnEdge(self):
        result = self.BottomLeft.State == TileTouchState.Space or self.BottomRight.State == TileTouchState.Space
        return result


class TiledSpriteCollider(object):
    """Checks the collosion state of a sprite."""

    def __init__(self):
        self.__currentState = None
        self._collideRect = None
        self._map = None

    def checkCollideAt(self, map, rect, position):

        result = CollisionResult(map, rect, position)
        return result

    def setPlayerPosition(self, position):
        if not self._map:
           self._map = ServiceLocator.getGlobalServiceInstance(ServiceNames.Map)
        if not self._collideRect:
            player = ServiceLocator.getGlobalServiceInstance(ServiceNames.Player)
            self._collideRect = player.collideRect

        self.__currentState = self.checkCollideAt(self._map, self._collideRect, position)
        pass

    @property
    def currentState(self):
        return self.__currentState







