from Utils import GetScreenSize
import pygame

class GameState(object):
    """states of the game"""
    def __init__(self):
        self.done = False
        self.size = GetScreenSize()
        self.clock = pygame.time.Clock()




