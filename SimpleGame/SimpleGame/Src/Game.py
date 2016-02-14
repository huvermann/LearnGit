# Main File.
import pygame
import os, sys
import logging
import Utils
from pygame.locals import *
from GameState import GameState
from Utils.ViewController import ViewController
from Utils.ServiceLocator import ServiceLocator

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
        self.configure()
        self.viewController = ViewController(self.screen, self.gameState)
        

    def configure(self):
        ServiceLocator.registerGlobalService("screen", self.screen)
        ServiceLocator.registerGlobalService("pygame", pygame)
        ServiceLocator.registerGlobalService("ViewController", self.viewController)
        ServiceLocator.registerGlobalService("gamestate", self.gameState)
        pass
    def cleanup(self):
        pygame.quit()

    def run(self):
        """Run the game loop"""
        # pygame.display.set_icon(pygame.image.load(Utils.DirHelper.getResourceFilePath("icon")))
        pygame.display.set_caption("SimpleGame")
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







