import Views.ViewModelBase

class View2(Views.ViewModelBase.ViewModelBase):
    """description of class"""
    def __init__(self, state, screen, changeViewCallback):
        super().__init__(state, screen, changeViewCallback)
        self.loadMap("Level1") # Todo: change map name



