import pygame
import os.path
import json
from GameState import GameState
from GameColors import GameColors
from Utils import UserEvents, TileMapManager
from Utils.DirHelper import getFontResourceFile
from pygame.color import THECOLORS

class ViewModelBase:
    """description of class"""
    def __init__(self, state, screen, changeViewCallback):
        """Inits the view."""
        self._callback = changeViewCallback
        self._state = state
        self._screen = screen
        self.colors = GameColors()
        self._demoText = "This is the base view"
        self._mapData = None
        self._tileSet = None
        self._mapManager = None
        self._positionX = 0
        self._positionY = 0
        self._keyboardSpeed = 10
        self._keyboardCountdown = 10
        self._doRendering = True
        self._viewModelName = None
        # Container for all sprites
        self._allSprites = pygame.sprite.Group()
        fontFile = getFontResourceFile("InknutAntiqua-Light")
        self._font = pygame.font.Font(fontFile, 12)

    def loadMap(self, mapName):
        self._mapManager = TileMapManager.TileMapManager(mapName)
        pass

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
            self._state.done = True
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
        elif event.type == pygame.JOYAXISMOTION:
            self.onJoystickEvent(event)
        elif event.type == pygame.JOYBUTTONDOWN:
            self.onJoystickEvent(event)
        else:
            print ("Unhandled: ", event.type)
        pass
    def onJoystickEvent(self, event):
        print("JoystickEvent")
        pass

    def onKeyboardEvent(self, event):
        """Handle the keyboard events."""
        print("A key was pressed: ", event.key)
        if event.key == pygame.K_q:
            # Q Pressed, quit game
            self._state.done = True
        elif event.key == pygame.K_1:
            self._callback("View1")
        elif event.key == pygame.K_2:
            self._callback("Level1")
        elif event.key == pygame.K_3:
            self._callback("Level2")
        elif event.key == pygame.K_a:
            self.ToggleRendering()

        pass

    def ToggleRendering(self):
        if self._doRendering:
            self._doRendering = False
        else:
            self._doRendering = True
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
                self._state.done = True
            elif event.type == 4 or event.type == 1:
                pass
            else:
                self.onEvent(event)
        pass

    def onMusicEvent(self, event):
        pass

    def keyboardJoystickChecker(self):
        """Raises the keyboard joystick event depending on the keyboardSpeed variable."""
        if self._keyboardCountdown == 0:
            self._keyboardCountdown = self._keyboardSpeed
            keyJoystickEvent = pygame.event.Event(UserEvents.EVENT_KEYJOYSTICK)
            pygame.event.post(keyJoystickEvent)
        else:
            self._keyboardCountdown = self._keyboardCountdown - 1
        pass


    def drawTiles(self):
        self._mapManager.drawTiles(self._screen, self._positionX, self._positionY)
        # Todo: Implement Keyboard and Joystick movement
        self._positionX += 3

    def drawScore(self):
        
        background = self._screen.convert()
        score = "x: {:d} y: {:d} fps: {}".format(self._positionX, self._positionY, str(self._state.clock.get_fps()))
        text = self._font.render(score, True, (255, 0, 0))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)
        self._screen.blit(background, (0,0))
        pygame.display.flip()
        pass
    
    def updateScreen(self):
        """Paint the screen."""
        pygame.draw.rect(self._screen, self.colors.GREEN, self._screen.get_rect())
        if self._doRendering:
            self.drawTiles()
            self.moveSprites()
        self.drawScore()
    
    def flipScreen(self):
        """Flip the screen."""
        pygame.display.flip()
        self._state.clock.tick(80)
    
    def moveSprites(self):
        """Moves all sprites."""
        self._allSprites.draw(self._screen)
        pass

    def _getViewModelName(self):
        """Getter for viewModelName property."""
        return self._viewModelName
    def _setViewModelName(self, value):
        """Sets the view model name property."""
        self._viewModelName = value
    viewModelName = property(_getViewModelName, _setViewModelName)









