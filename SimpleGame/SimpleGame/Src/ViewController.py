from Views.ViewStart import ViewStart
from Views.View2 import *


class ViewController(object):
    """description of class"""
    def __init__(self, screen, gameState):
        """Initializes the view controler"""
        self.screen = screen
        self.gameState = gameState
        self.viewList = {}
        self.currentView = None
        self.changeView("View1")
        #self.currentView = self.viewFactory("ViewStart")
        #self.viewList = {'ViewStart': self.currentView};
        pass
    
    def ChangeViewCallback(self, viewName):
        """Called by the view if the view is going to change."""
        print("Changing to view: ", viewName)
        # Todo: Implement change the view
        self.changeView(viewName)
        pass

    def changeView(self, viewName):
        """Changes the view by name."""
        #newclass = ViewStart(self.gameState, self.screen, self.ChangeViewCallback)
        #self.currentView = newclass
        if viewName in self.viewList:
            self.currentView = self.viewList[viewName]
            return self.currentView
        else:
            newView = self.viewFactory(viewName)
            if newView:
                self.currentView = newView
                self.viewList[viewName] = newView

        return newView
    def viewFactory(self, viewName):
        """Creates a view by name."""
        if viewName == "View1":
            return ViewStart(self.gameState, self.screen, self.ChangeViewCallback)
        elif viewName == "Level1":
            return View2(self.gameState, self.screen, self.ChangeViewCallback)
        # Todo implement all views
        else: 
            return None


    def run(self):
        """Run the view."""
        self.currentView.runView()



        


