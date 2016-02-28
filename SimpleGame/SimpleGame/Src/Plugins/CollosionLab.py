from Utils.ViewPluginBase import ViewPluginBase
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.gui.TextLabel import TextLabel
from Tiled.TiledMap import TiledMap
from Tiled.TiledSpriteCollider import TiledSpriteCollider
import pygame

class CollosionLab(ViewPluginBase):
    """Pluginin to test collosions with background."""
    def __init__(self):
        super().__init__()
        self._player = None
        self._tileCollider = None
        self._map = None
        self._screenRect = None
        self.buttons = pygame.sprite.Group()
        self.UpButton = TextLabel(550, 300, "Oben")
        self.buttons.add(self.UpButton)
        self.DownButton = TextLabel(550, 350, "Unten")
        self.buttons.add(self.DownButton)
        self.LeftButton = TextLabel(500, 325, "Links")
        self.buttons.add(self.LeftButton)
        self.RightButton = TextLabel(580, 325, "Rechts")
        self.RightButton.buttonColor = (255, 0,0)
        self.buttons.add(self.RightButton)



    def initializePlugin(self, parentView):
        super().initializePlugin(parentView)
        if not self._player:
            self._player = ServiceLocator.getGlobalServiceInstance(ServiceNames.Player)
        self._map = ServiceLocator.getGlobalServiceInstance(ServiceNames.Map)
        self._screenRect = self._screen.get_rect()


    def drawPlugin(self):
        collider = TiledSpriteCollider()
        position = self._viewPointer.getPlayerMapPosition()

        Info = collider.checkCollideAt(self._map, self._player.collideRect, position)

        
        red =  (255,0,0)
        green = (0,255,0)
        
        Left = self._viewPointer.mapPositionToScreenOffset(Info._checkPoints.Left)
        Right = self._viewPointer.mapPositionToScreenOffset(Info._checkPoints.Right)
        BottomLeft = self._viewPointer.mapPositionToScreenOffset(Info._checkPoints.BottomLeft)
        BottomRight = self._viewPointer.mapPositionToScreenOffset(Info._checkPoints.BottomRight)
        Center = self._viewPointer.mapPositionToScreenOffset(Info._checkPoints.Center)
        TopLeft = self._viewPointer.mapPositionToScreenOffset(Info._checkPoints.TopLeft)
        TopRight = self._viewPointer.mapPositionToScreenOffset(Info._checkPoints.TopRight)


        pygame.draw.circle(self._screen, red, (Left.left, Left.top), 2)
        pygame.draw.circle(self._screen, red, (Right.left, Right.top), 2)
        pygame.draw.circle(self._screen, red, (BottomLeft.left, BottomLeft.top), 2)
        pygame.draw.circle(self._screen, red, (BottomRight.left, BottomRight.top), 2)
        pygame.draw.circle(self._screen, red, (TopLeft.left, TopLeft.top), 2)
        pygame.draw.circle(self._screen, red, (TopRight.left, TopRight.top), 2)
        pygame.draw.circle(self._screen, green, (Center.left, Center.top), 2)

        #print("Is Grounded: {0}; Is Docked: {1}, Upper: {2}; upperDock: {3}".format(Info.isGrounded, test, Info.isUpperLayerTouched, Info.isUpperLayerDocked))
        if Info.isUpperLayerTouched:
            self.UpButton.buttonColor = red
        else:
            self.UpButton.buttonColor = green

        if Info.isGrounded:
            self.DownButton.buttonColor = red
        else:
            self.DownButton.buttonColor = green

        if Info.isLeftTouched:
            self.LeftButton.buttonColor = red
        else:
            self.LeftButton.buttonColor = green

        if Info.isRightToched:
            self.RightButton.buttonColor = red
        else:
            self.RightButton.buttonColor = green


        self.buttons.draw(self._screen)
        return super().drawPlugin()



