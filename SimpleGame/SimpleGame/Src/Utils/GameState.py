from Utils import Utils
import pygame

class GameState(object):
    """states of the game"""
    def __init__(self):
        self.done = False
        self.size = Utils.GetScreenSize()
        self.clock = pygame.time.Clock()
        self.points = 0
        self.lifes = 3
        self.energy = 100





