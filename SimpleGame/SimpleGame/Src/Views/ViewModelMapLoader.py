#obsolete class. Remove!
from Utils.TmxTileMapViewModel import TmxTileMapViewModel

class ViewModelMapLoader(TmxTileMapViewModel):
    """View Model to load any views by name."""
    def __init__(self, viewName, screen):
        return super().__init__(viewName, screen)

    #def __init__(self,viewModelName, state, screen, changeViewCallback):
    #    super().__init__(state, screen, changeViewCallback)
    #    self.loadMap(viewModelName)
    #    self.viewModelName = viewModelName



