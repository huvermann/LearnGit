# Main File.
import pygame
import os, sys
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
        self.joystick = self.initJoystick()
        self.colors = GameColors()
        self.gameState = GameState()
        self.screen = pygame.display.set_mode(self.gameState.size)
        self.viewController = ViewController(self.screen, self.gameState)


    def cleanup(self):
        pygame.quit()

    def run(self):
        """Run the game loop"""
        #pygame.display.set_icon(pygame.image.load(Utils.DirHelper.getResourceFilePath("icon")))
        pygame.display.set_caption("SimpleGame")
        try:
            while not self.gameState.done:
                self.viewController.currentView.runView()
        except Exception as e:
            print(e)
            self.gameState.done = True


    def initJoystick(self):
        joystick = None
        joystickCount = pygame.joystick.get_count()
        if joystickCount == 0:
            print ("No joystick found")
        else:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        return joystick

if __name__ == "__main__":
    game = MainGame()
    game.run()
    game.cleanup()







