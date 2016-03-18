from Utils.ViewPluginBase import ViewPluginBase
import pygame
from Utils.ViewPointer import ViewPoint
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Sprites.BloobSprite import BloobSprite
from SpriteIntelligence.Dropdown2AI import Dropdown2AI


class DropDownSimulator(ViewPluginBase):
    """description of class"""
    def __init__(self):
        super().__init__()
        self.map = ServiceLocator.getGlobalServiceInstance(ServiceNames.Map)
        self._dropLines = []

    def initializePlugin(self, parentView):
        super().initializePlugin(parentView)
        self.registerEventHandler()

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.onMouseButtonDown(event)

    def onMouseButtonDown(self, event):
        print(event)
        point = ViewPoint(event.pos[0], event.pos[1])
        screenOffset = self._viewPointer.screenPosition
        mapPos = ViewPoint(screenOffset.left + point.left, screenOffset.top+point.top)
        newCoin = BloobSprite()
        newCoin.configureFromProperties({})
        newCoin.intelligence = Dropdown2AI(newCoin, {})
        newCoin.x = mapPos.left
        newCoin.y = mapPos.top
        self._curentView.allSprites.add(newCoin)
        self._curentView.objectSprites.add(newCoin)
        print("-------- Sprite created -----------")
        newCoin.rect = pygame.Rect(0,0,32,32)
        p1 = point
        wtg = newCoin.intelligence._mapScanner.getWayToGround()
        p2 = ViewPoint(p1.left, p1.top + wtg)
        self._dropLines.append((p1, p2))

    def drawPlugin(self):
        for line in self._dropLines:
            pygame.draw.line(self._screen, (255,0,0), (line[0].left, line[0].top), (line[1].left, line[1].top))
        return super().drawPlugin()




