#from Views.ViewStart import ViewStart
#from Views.View2 import *
#from Views.Level2 import *
from Views.ViewModelMapLoader import ViewModelMapLoader
import sys
import logging


class ViewController(object):
    """description of class"""
    def __init__(self, screen, gameState):
        """Initializes the view controler"""
        self.screen = screen
        self.gameState = gameState
        self.viewList = {}
        self.currentView = None
        self.changeView("Level2")
        pass
    
    def ChangeViewCallback(self, viewName):
        """Called by the view if the view is going to change."""
        print("Changing to view: ", viewName)
        # Todo: Implement change the view
        self.changeView(viewName)
        pass

    def changeView(self, viewName):
        """Changes the view by name."""
        if viewName in self.viewList:
            self.currentView = self.viewList[viewName]
            return self.currentView
        else:
            try:
                newView = self.viewFactory(viewName)
            except Exception as e:
                newView = None
                logging.error(e)
                raise

            if newView:
                self.currentView = newView
                self.viewList[viewName] = newView

        return newView
    def viewFactory(self, viewName):
        """Creates a view by name."""
        if viewName == "View1x":
            return ViewStart(self.gameState, self.screen, self.ChangeViewCallback)
        elif viewName == "Level1x":
            return View2(self.gameState, self.screen, self.ChangeViewCallback)
        # Todo implement all views
        else:
            # Loads any model 
            return ViewModelMapLoader(viewName)


    def run(self):
        """Run the view."""
        self.currentView.runView()



        


