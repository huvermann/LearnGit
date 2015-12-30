from Views.ViewModelBase import ViewModelBase 

class ViewModelMapLoader(ViewModelBase):
    """View Model to load any views by name."""
    def __init__(self,viewModelName, state, screen, changeViewCallback):
        super().__init__(state, screen, changeViewCallback)
        self.loadMap(viewModelName)
        self.viewModelName = viewModelName



