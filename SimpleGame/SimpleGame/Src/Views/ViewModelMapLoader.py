#obsolete class. Remove!
from Utils.TmxTileMapViewModel import TmxTileMapViewModel

class ViewModelMapLoader(TmxTileMapViewModel):
    """View Model to load any views by name."""
    def __init__(self, viewName):
        return super().__init__(viewName)

    def drawScore(self):
        #remove this!
        pass

    def drawInfoText(self):
        #remove this!
        pass

        




