from Utils import Utils
#from Utils import GetScreenSize
import pygame

class GameState(object):
    """states of the game"""
    def __init__(self):
        self.done = False
        self.size = Utils.GetScreenSize()
        self.clock = pygame.time.Clock()




