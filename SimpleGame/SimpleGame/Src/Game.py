# Main File.
import pygame
import os, sys
import logging
import Utils
from pygame.locals import *
from GameColors import GameColors
from GameState import GameState
from ViewController import ViewController

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

class MainGame:
    """The main game class"""
    def __init__(self):
        """Initialization of the main class."""
        logging
        pygame.init()
        logging.debug('Game started!')
        #self.joystick = self.initJoystick()
        self.colors = GameColors()
        self.gameState = GameState()
        self.screen = pygame.display.set_mode(self.gameState.size)
        self.viewController = ViewController(self.screen, self.gameState)



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







