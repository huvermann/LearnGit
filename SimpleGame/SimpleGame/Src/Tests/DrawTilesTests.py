import unittest
from Utils.TileMapManager import TileMapManager
from Tests.TileTestHelper import TileTestHelper



class SceenMock():
    def __init__(self):
        self.blitCalled = False
        self.surface = None
        self.position = None
        pass


    
    def blit(self, surface, position):
        """Mock the blit method."""
        self.blitCalled = True
        self.surface = surface
        self.position = position
        pass

class TileImageMock():
    def __init__(self, column, row):
        self.row = row
        self.column = column

    def __eq__(self, other):
        result = False
        if isinstance(other, self.__class__):
            if self.column == other.column:
                if self.row == other.row:
                    result = True
        return result

class TileMapTestClass(TileMapManager):
    def __init__(self):
        pass

    def mockCalcTile(self, offset, grid):
        return 0

    def mockTileMap(self, width, height):
        """Creates a numbered tileset."""
        self._tileMapArray = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(y*height + x)
                #row.append(TileImageMock(x, y))
            self._tileMapArray.append(row)



    def initTestItem(self, tileHeigth, tileWidth, tilesWide, tilesHeigth, tilesCountx, tilesCounty, tileSetWith, tileSetHeight):
        self._tileHeight = tileHeigth
        self._tileWidth = tileWidth
        self._mapData = {'tileswide' : tilesWide, 'tileshigh' : tilesHeigth, 'tileheight' : tileHeigth, 'tilewidth' : tileWidth}
        self._getcount = (tilesCountx, tilesCounty)
        self._tileSetWith = tileSetWith
        self._tileMapArray = []
        cnt = 0
        self._backgroundImage = None
        for y in range(tilesCounty):
            row = []
            self._tileMapArray.append(row)
            for x in range(tilesCountx):
                row.append(0)
                cnt += 1
        
        self._tileSet = []

        cnt = 0
        for y in range(tileSetHeight):
            row = []
            self._tileSet.append(row)
            for x in range(tileSetWith):
                row.append(cnt)
                cnt += 1

        pass

    def getTileCount(self, screen):
        return self._getcount
        pass





class Test_DrawTilesTests(unittest.TestCase):
    def setUp(self):
        self._testItem = TileMapTestClass()
        self._screenMock = SceenMock()


    def test_DrawTiles(self):
        data = TileTestHelper()
        data.tilesCountx = 10
        data.tilesCounty = 10
        self._testItem.calcTile = self._testItem.mockCalcTile
        self._testItem.initTestItem(data.tileHeigth, data.tileWidth, data.tilesWide, data.tilesHeight, data.tilesCountx, data.tilesCounty, data.tileSetWith, data.tileSetHeight)
        self._testItem.drawTiles(self._screenMock, (data.xOffset, data.yOffset))
        self.assertTrue(self._screenMock.blitCalled)
        pass

    def test_calcTileIndexNumber(self):
        data = TileTestHelper()

        self._testItem.initTestItem(data.tileHeigth, data.tileWidth, data.tilesWide, data.tilesHeight, data.tilesCountx, data.tilesCounty, data.tileSetWith, data.tileSetHeight)
        self._testItem.mockTileMap(10,10)
        tileIndex = self._testItem.calcTile((0,0), (0,0))
        self.assertEqual(0, tileIndex, "Expected tile index to be 0")



         

        

if __name__ == '__main__':
    unittest.main()
