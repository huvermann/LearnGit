#obsolete class. Remove!
from Utils.TmxTileMapViewModel import TmxTileMapViewModel

class ViewModelMapLoader(TmxTileMapViewModel):
    """View Model to load any views by name."""
    def __init__(self, viewName, screen):
        return super().__init__(viewName, screen)

    #def updateSprites(self):
    #    #Remove this
    #    pass

    #def drawSprites(self):
    #    #remove this
    #    pass

    def drawScore(self):
        #remove this!
        pass

    def drawInfoText(self):
        #remove this!
        pass
    def checkClashes(self):
        #remove this
        pass

        




