from Utils.ViewPluginBase import ViewPluginBase
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.gui.TextLabel import TextLabel
import pygame

class ShowTileNumbers(ViewPluginBase):
    """Displays the tile index and numbers on the screen"""
    def __init__(self):
        super().__init__()
        self._map = ServiceLocator.getGlobalServiceInstance(ServiceNames.Map)
        self.cache = {}
        self._buttons = pygame.sprite.Group()
        self.button = TextLabel(620,110, "Module is OFF")
        self.button.onClick=self.onClickHandler
        self._buttons.add(self.button)
        self.viewMode = 0

    def onClickHandler(self):
        if self.viewMode == 0:
            self.viewMode = 1
            self.button.caption = 'Module is ON'

        elif self.viewMode == 1:
            self.viewMode = 2
            self.button.caption = 'Tile XY'
        else:
            self.viewMode = 0
            self.button.caption = "Module is OFF"

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.handleOnMouseClick(pos)
            #if event.type == self.TIMEREVENT:
            #    self._calculationDirty = True
        pass

    def handleOnMouseClick(self, position):
        for button in self._buttons:
            if button.rect.collidepoint(position):
                button.onClick()
        pass

       

    def createLabel(self, caption):
        if caption in self.cache:
            return self.cache[caption]

        font = pygame.font.Font(None, 14)
        text = font.render(caption, 1, (255, 10, 10))
        textpos = text.get_rect()
        image = pygame.Surface([textpos.width, textpos.height])
        image.set_colorkey((0,0,0))
        image.blit(text, textpos)
        self.cache[caption] = image
        return image

    def drawAddressNumbers(self):
        th = self._map.tileHeight
        tw = self._map.tileWidth
        offset = self._viewPointer.screenPosition.copy()
        shiftx = offset.left % tw
        shifty = offset.top % th

        rangex = self._screen.get_width()//tw
        rangey = self._screen.get_height()//th

        for y in range(0, rangey+2):
            py=y*th-shifty
            for x in range(0, rangex+2):
                tileIndex=self._map.calcTileMapXY(offset, (x,y))
                label = self.createLabel("{0}, {1}".format(tileIndex[0], tileIndex[1]))
                self._screen.blit(label, (x*tw-shiftx, py))
        
        pass


    def drawTileNumbers(self):
        th = self._map.tileHeight
        tw = self._map.tileWidth
        offset = self._viewPointer.screenPosition.copy()
        shiftx = offset.left % tw
        shifty = offset.top % th

        rangex = self._screen.get_width()//tw
        rangey = self._screen.get_height()//th

        for y in range(0, rangey+2):
            py=y*th-shifty
            for x in range(0, rangex+2):
                tileIndex=self._map.calcTileMapIndex(offset, (x,y))
                label = self.createLabel("{0}".format(tileIndex))
                self._screen.blit(label, (x*tw-shiftx, py))
                 

    def drawPlugin(self):
        if not self._curentView:
            self.registerEventHandler()

        if self.viewMode == 1:
            self.drawTileNumbers()
        elif self.viewMode == 2:
            self.drawAddressNumbers()
        self._buttons.draw(self._screen)
        pass

    def update(self):
        return super().update()


