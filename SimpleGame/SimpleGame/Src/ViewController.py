from Views.ViewStart import ViewStart


class ViewController(object):
    """description of class"""
    def __init__(self, screen, gameState):
        """Initializes the view controler"""
        self.screen = screen
        self.gameState = gameState
        self.currentView = self.changeView("ViewStart")
        self.viewList = {'ViewStart': self.currentView};



    def changeView(self, viewName):
        """Changes the view by name."""
        newclass = ViewStart(self.gameState, self.screen)
        self.currentView = newclass
        return newclass

    def run(self):
        """Run the view."""
        self.currentView.runView()



        


