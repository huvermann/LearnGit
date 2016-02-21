# Main File.
import pygame
import os, sys
import logging
import Utils
from pygame.locals import *
from GameState import GameState
from Utils.ViewController import ViewController
from Utils.ServiceLocator import ServiceLocator, ServiceNames

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
        #ServiceLocator.registerGlobalService("pygame", pygame)
        ServiceLocator.registerGlobalService(ServiceNames.ViewController, self.viewController)
        ServiceLocator.registerGlobalService(ServiceNames.Gamestate, self.gameState)
        pass
    def cleanup(self):
        pygame.quit()

    def run(self):
        """Run the game loop"""
        # pygame.display.set_icon(pygame.image.load(Utils.DirHelper.getResourceFilePath("icon")))
        pygame.display.set_caption("SimpleGame")
        # Start-Screen
        #self.viewController.changeView("Training")
        self.viewController.changeView("Level2")
        try:
            while not self.gameState.done:
                self.viewController.currentView.runView()
        except Exception as e:
            logging.error(e)
            self.gameState.done = True

if __name__ == "__main__":
    game = MainGame()
    game.run()
    game.cleanup()







