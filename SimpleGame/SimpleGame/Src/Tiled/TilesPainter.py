import pygame
from Tiled.TiledMap import TiledMap 
from Utils.ViewPointer import ViewPointer, ViewPoint


class TilesPainter(object):
    """description of class"""
    @staticmethod
    def drawTiles(screen, tileMap, viewPointer):
        """Draw the tiles on the screen."""
        assert isinstance(screen, pygame.Surface), "Screen must be of type pygame.Surface."
        assert isinstance(tileMap, TiledMap), "tileMap must be of type Tiled.TileMap."
        assert isinstance(viewPointer, ViewPointer), "viewPointer must be of type ViewPointer."
        th = tileMap.tileHeight
        tw = tileMap.tileWidth

        offset = viewPointer.screenPosition
        shiftx = offset.left % tw
        shifty = offset.top % th

        rangex = screen.get_width()//tw
        rangey = screen.get_height()//th

        for y in range(0, rangey+2):
            py=y*th-shifty
            for x in range(0, rangex+2):
                bgTileIndex = tileMap.calcTileMapIndex(offset, (x,y), "BackgroundMap")
                if bgTileIndex > 0:
                    image = tileMap.getTileImage(bgTileIndex)
                    screen.blit(image, (x*tw-shiftx, py))
                tileIndex=tileMap.calcTileMapIndex(offset, (x,y))
                if tileIndex > 0:
                    image = tileMap.getTileImage(tileIndex)
                    screen.blit(image, (x*tw-shiftx, py))
        pass

    @staticmethod
    def drawBackground(screen, tileMap, viewPointer):
        """Draws the background image."""
        assert isinstance(screen, pygame.Surface), "Screen must be of type pygame.Surface."
        assert isinstance(tileMap, TiledMap), "tileMap must be of type Tiled.TileMap."
        assert isinstance(viewPointer, ViewPointer), "viewPointer must be of type ViewPointer."
        image = tileMap.backgroundImageSurface
        screenRect = screen.get_rect()
        imageRect = image.get_rect()
        mapWidth = tileMap.width * tileMap.tileWidth
        mapHeight = tileMap.height * tileMap.tileHeight
        #offset = viewPointer.screenOffset
        offset = viewPointer.screenPosition

        # Don´t scroll the background in y direction
        yoffset = offset.top
        if yoffset < 0:
            xoffset = 0
        elif yoffset > mapHeight:
            yoffset = mapHeight

        screenRect.top = int((imageRect.size[1] - screenRect.size[1]) / mapHeight * (yoffset % mapHeight))
        screenRect.left = int((imageRect.size[0] - screenRect.size[0]) / mapWidth * (offset.top % mapWidth))
        
        partImage = image.subsurface(screenRect)
        screen.blit(partImage, (0,0))

        pass







