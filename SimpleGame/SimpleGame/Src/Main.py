﻿import os, sys
import pygame
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
        pygame.init()
        self.colors = GameColors()
        self.gameState = GameState()
  
        self.screen = pygame.display.set_mode(self.gameState.size)
        self.viewController = ViewController(self.screen, self.gameState)

    def cleanup(self):
        pygame.quit()

    def run(self):
        """Run the game loop"""
        
        pygame.display.set_caption("SimpleGame")
        while not self.gameState.done:
            self.viewController.currentView.runView()

if __name__ == "__main__":
    game = MainGame()
    game.run()
    game.cleanup()






