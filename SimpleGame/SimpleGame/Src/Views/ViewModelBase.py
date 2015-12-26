import pygame
import os.path
import json
from Views.DirHelper import getResourceFilePath
from GameState import GameState
from GameColors import GameColors

class ViewModelBase:
    """description of class"""
    def __init__(self, state, screen):
        """Inits the view."""
        self.state = state
        self.screen = screen
        self.colors = GameColors()
        self.mapData = None
        # Container for all sprites
        self.allSprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)

    def loadMap(self, mapName):
        self.mapFileName = getResourceFilePath(mapName + ".map")
        self.mapImageFileName = getResourceFilePath(mapName + ".png")
        if os.path.isfile(self.mapFileName):
            # Load the map file
            with open(self.mapFileName) as data_file:
                self.mapData = json.load(data_file)
        else:
            # File not exist
            raise FileNotFoundError(self.mapFileName)
        if os.path.isfile(self.mapImageFileName):
            # Load the map image
            self.mapImage=pygame.image.load(self.mapImageFileName)
        else:
            raise FileNotFoundError(self.mapImageFileName)

    def runView(self):
        """Runs the view."""
        self.handleEvent()
        self.updateScreen()
        self.flipScreen()
        pass

    def handleEvent(self):
        """Handles the events..."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.done = True
    
    def updateScreen(self):
        """Paint the screen."""
        
        self.screen.fill(self.colors.WHITE)
        background = self.screen.convert()
        text = self.font.render("The base screen", 1, (10,10,10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)
        self.screen.blit(background, (0,0))
        

        self.moveSprites()
    
    def flipScreen(self):
        """Flip the screen."""
        pygame.display.flip()
        self.state.clock.tick(60)
    
    def moveSprites(self):
        """Moves all sprites."""
        self.allSprites.draw(self.screen)
        pass









