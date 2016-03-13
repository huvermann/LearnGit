# Main File.
import pygame
import os, sys, getopt
import logging
import Utils
from pygame.locals import *
from Utils.GameState import GameState
from Utils.ViewController import ViewController
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.BeamPointRegistry import BeamPointRegistry

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

class MainGame:
    """The main game class"""
    def __init__(self):
        """Initialization of the main class."""
        logging.basicConfig(filename="gamelog.log", level=logging.DEBUG)
        logging.info("Started")
        pygame.init()
        logging.debug('Game started!')
        self.gameState = GameState()
        self.screen = pygame.display.set_mode(self.gameState.size)
        self.viewController = None
        self.viewController = ViewController()
        self.configure()
        

    def configure(self):
        ServiceLocator.registerGlobalService(ServiceNames.Screen, self.screen)
        ServiceLocator.registerGlobalService(ServiceNames.PyGame, pygame)
        ServiceLocator.registerGlobalService(ServiceNames.ViewController, self.viewController)
        ServiceLocator.registerGlobalService(ServiceNames.Gamestate, self.gameState)
        ServiceLocator.registerGlobalService(ServiceNames.BeamPoints, BeamPointRegistry())
        pass
    def cleanup(self):
        pygame.quit()

    def run(self):
        """Run the game loop"""
        # pygame.display.set_icon(pygame.image.load(Utils.DirHelper.getResourceFilePath("icon")))
        pygame.display.set_caption("SimpleGame")
        defaultStartView = "DemoStart"
        # Start-Screen
        viewName = self.parseViewNameFromCommandArgs()
        if viewName:
            self.viewController.changeView(viewName)
        else:
            self.viewController.changeView(defaultStartView)

        # Initialize the first save poin
        try:
            while not self.gameState.done:
                self.viewController.currentView.runView()
        except Exception as e:
            logging.error(e)
            self.gameState.done = True

    def parseViewNameFromCommandArgs(self):
        result = None
        opts, args = getopt.getopt(sys.argv[1:], "v:", ["view="])
        for o, a in opts:
            if o == "-v":
                result = a
            if o == "view=":
                result = a

        return result

if __name__ == "__main__":
    game = MainGame()
    game.run()
    game.cleanup()







