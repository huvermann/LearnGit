import pygame
import os.path
import json
from Views.DirHelper import getResourceFilePath
from GameState import GameState
from GameColors import GameColors
from Utils import UserEvents

class ViewModelBase:
    """description of class"""
    def __init__(self, state, screen, changeViewCallback):
        """Inits the view."""
        self.callback = changeViewCallback
        self.state = state
        self.screen = screen
        self.colors = GameColors()
        self.demoText = "This is the base view"
        self.mapData = None
        self.tileSet = None
        self.positionX = 0
        self.positionY = 0
        self.keyboardSpeed = 10
        self.keyboardCountdown = 10
        # Container for all sprites
        self.allSprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)

    def loadTileSet(self, filename, width, height):
        image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        tileset = []
        for tile_x in range(0, image_width//width):
            line = []
            tileset.append(line)
            for tile_y in range(0, image_height//height):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(image.subsurface(rect))
        return tileset

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
            self.tileSet = self.loadTileSet(self.mapImageFileName, 16, 16)
        else:
            raise FileNotFoundError(self.mapImageFileName)

    def runView(self):
        """Runs the view."""
        self.keyboardJoystickChecker()
        self.handleEvents()
        self.updateScreen()
        self.flipScreen()
        pass


    def onEvent(self, event):
        """Handle events."""
        if event.type == pygame.QUIT:
            self.state.done = True
        elif event.type == pygame.KEYDOWN:
            self.onKeyboardEvent(event)
        elif event.type == UserEvents.EVENT_MUSIC:
            self.onMusicEvent(event)
        elif event.type == UserEvents.EVENT_CHANGEVIEW:
            self.onViewChange(event)
        elif event.type == UserEvents.EVENT_NOISE:
            self.onNoiseEvent(event)
        elif event.type == UserEvents.EVENT_KEYJOYSTICK:
            self.onKeyboardJoystickEvent(event)

    def onKeyboardEvent(self, event):
        """Handle the keyboard events."""
        print("A key was pressed: ", event.key)
        if event.key == pygame.K_q:
            # Q Pressed, quit game
            self.state.done = True
        elif event.key == pygame.K_1:
            self.callback("View1")
        elif event.key == pygame.K_2:
            self.callback("View2")

        pass
    def onKeyboardJoystickEvent(self, event):
        #print("Keyboard Joystick ckecked.")
        pass

    def onNoiseEvent(self, event):
        """Start a sound."""
        # Todo: implement play sound.
        pass

    def onViewChange(self, event):
        """View is going to be changed."""
        # Todo: Implement change the view.
        pass

    def handleEvents(self):
        """Handle all events in event list"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.done = True
            else:
                self.onEvent(event)
        pass

    def onMusicEvent(self, event):
        pass

    def keyboardJoystickChecker(self):
        """Raises the keyboard joystick event depending on the keyboardSpeed variable."""
        if self.keyboardCountdown == 0:
            self.keyboardCountdown = self.keyboardSpeed
            keyJoystickEvent = pygame.event.Event(UserEvents.EVENT_KEYJOYSTICK)
            pygame.event.post(keyJoystickEvent)
        else:
            self.keyboardCountdown = self.keyboardCountdown - 1
        pass


    def drawTiles(self):
        # Todo: draw all tiles
        self.screen.blit(self.tileSet[0][0], (-2,0))
        self.screen.blit(self.tileSet[1][0], (-2,16))
    
    def updateScreen(self):
        """Paint the screen."""
        
        self.screen.fill(self.colors.WHITE)
        background = self.screen.convert()
        text = self.font.render(self.demoText, 1, (10,10,10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)
        self.screen.blit(background, (0,0))
        self.drawTiles()
        

        self.moveSprites()
    
    def flipScreen(self):
        """Flip the screen."""
        pygame.display.flip()
        self.state.clock.tick(60)
    
    def moveSprites(self):
        """Moves all sprites."""
        self.allSprites.draw(self.screen)
        pass









