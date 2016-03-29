import pygame
import os, sys, getopt
import logging
import Utils
from pygame.locals import *
from Utils.GameState import GameState
from Utils.ViewController import ViewController
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.BeamPointRegistry import BeamPointRegistry

class TileGame(object):
    """The Main Game Class."""
    def __init__(self, gameName, startViewName):
        """Initialization of the main class."""
        self.gamName = gameName
        self.startViewName = startViewName

        logging.basicConfig(filename="gamelog.log", level=logging.DEBUG)
        logging.info("Started")
        if not pygame.font: logging.warn('Warning, fonts disabled')
        if not pygame.mixer: logging.warn('Warning, sound disabled')

        pygame.init()
        self.gameState = GameState()
        self.__setIcon()
        self.screen = pygame.display.set_mode(self.gameState.size)
        self.viewController = None
        self.viewController = ViewController()
        self.configure()

    def __setIcon(self):
        """Set the window icon."""
        img = Utils.DirHelper.getImageResourceFile("dog")
        pygame.display.set_caption("CoolVerine", img)
        pygame.display.set_icon(pygame.image.load(img))
        pass

    def configure(self):
        ServiceLocator.registerGlobalService(ServiceNames.Screen, self.screen)
        ServiceLocator.registerGlobalService(ServiceNames.PyGame, pygame)
        ServiceLocator.registerGlobalService(ServiceNames.ViewController, self.viewController)
        ServiceLocator.registerGlobalService(ServiceNames.Gamestate, self.gameState)
        ServiceLocator.registerGlobalService(ServiceNames.BeamPoints, BeamPointRegistry())
        pass

    def cleanup(self):
        pygame.quit()
        pass

    def run(self):
        """Run the game loop"""
        
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





