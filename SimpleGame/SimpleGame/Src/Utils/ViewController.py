#from Views.ViewStart import ViewStart
#from Views.View2 import *
#from Views.Level2 import *
from Views.ViewModelMapLoader import ViewModelMapLoader
import sys
import logging
from Utils.ServiceLocator import ServiceLocator, ServiceNames


class ViewController(object):
    """description of class"""
    def __init__(self):
        """Initializes the view controler"""
        self.viewList = {}
        self._currentView = None
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
            if self._currentView:
                self._currentView.suspendView()

            self.viewList[viewName].unSuspendView()
            self._currentView = self.viewList[viewName]
            ServiceLocator.registerGlobalService(ServiceNames.CurrentView, self._currentView)
            
            return self._currentView
        else:
            try:
                newView = self.viewFactory(viewName)
            except Exception as e:
                newView = None
                logging.error(e)
                raise

            if newView:
                self._currentView = newView
                ServiceLocator.registerGlobalService(ServiceNames.CurrentView, self._currentView)
                self.viewList[viewName] = newView
                newView.initializeView()

        return newView
    def viewFactory(self, viewName):
        """Creates a view by name."""
        #Todo: Remove obsolete views
        if viewName == "View1x":
            return ViewStart(self.gameState, self.screen, self.ChangeViewCallback)
        elif viewName == "Level1x":
            return View2(self.gameState, self.screen, self.ChangeViewCallback)
        # Todo: Implement new View Factory
        else:
            # Loads any model 
            return ViewModelMapLoader(viewName)


    def run(self):
        """Run the view."""
        self._currentView.runView()

    @property
    def currentView(self):
        return self._currentView




        


