import Views.ViewModelBase

class Level2(Views.ViewModelBase.ViewModelBase):
    """description of class"""
    def __init__(self, state, screen, changeViewCallback):
        super().__init__(state, screen, changeViewCallback)
        self.loadMap("Level2") # Todo: change map name
        self._demoText = "Dies ist Level2"


