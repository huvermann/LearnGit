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




