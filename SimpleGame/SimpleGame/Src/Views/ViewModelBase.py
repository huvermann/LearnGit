import pygame
import os.path
import logging
from decimal import Decimal
import json
from GameState import GameState
from Utils import UserEvents, TileMapManager
from Utils.DirHelper import getFontResourceFile, getConfigurationFile
from pygame.color import THECOLORS
from Utils.KeyboardInputManager import KeyboardInputManager
from Utils.JoystickInputManager import JoystickInputManager
from Utils.MusicPlayer import MusicPlayer
from Utils.Constants import ConfigKey, ViewNames, Corners
from Sprites.SpriteFactory import createSpriteInstance
from Utils.JoystickStates import JoystickEvents
from Utils.MapPosition import MapPosition



class ViewModelBase:
    """description of class"""
    def __init__(self, state, screen, changeViewCallback):
        """Inits the view."""
        self._callback = changeViewCallback
        self._state = state
        self._screen = screen
        #self.colors = GameColors()
        #self._mapData = None
        self._tileSet = None
        self._mapManager = None
        self._position = MapPosition(0,0)
        self._moveVectorX = 0
        self._moveVectorY = 0
        self._viewModelName = None
        self._configuration = None
        self._musicPlayer = None
        self._playerSprite = None
        self._moveStartTime = None
        self._infoText = "Info"
        self._backgroundImageFileName = "background.png" # default bg image name

        # Container for all sprites
        self._allSprites = pygame.sprite.Group()
        self._movingSprites = pygame.sprite.Group()

        if self._playerSprite:
            self._allSprites.add(self._playerSprite)
        fontFile = getFontResourceFile("InknutAntiqua-Light")
        self._font = pygame.font.Font(fontFile, 12)
        self._keyboardEventHandler = self._initKeyboardManager()
        # Todo: implement JoystickEventHandler
        self._joystickEventHandler = self._initJoystickManager()

    def _loadConfiguration(self, viewModelName):
        """Loads the configuration file."""
        result = None
        file = getConfigurationFile(viewModelName)
        if os.path.isfile(file):
            with open(file) as data_file:
                result = json.load(data_file)
        return result

        pass


    def _initKeyboardManager(self):
        """Assigns the event handler for keys."""
        result = KeyboardInputManager.default()
        result.mapCallbacks(
            self.onKeyRelease,
            self.onMoveRight,
            self.onMoveLeft,
            self.onMoveUp,
            self.onMoveDown,
            self.onJump,
            self.onJumpButtonRelease,
            self.onKeyStart,
            self.onKeyExit)

        return result

    def _initJoystickManager(self):
        result = JoystickInputManager()
        result.mapCallbacks(
            self.onKeyRelease,
            self.onMoveRight,
            self.onMoveLeft,
            self.onMoveUp,
            self.onMoveDown,
            self.onJump,
            self.onJumpButtonRelease,
            self.onKeyStart,
            self.onKeyExit)
        return result


    def onKeyRelease(self, event):
        logging.debug("Key release")
        print("Key released")
        self._moveVectorX = 0
        self._moveVectorY = 0
        self.saveStartingPosition()
        self._playerSprite.joystickChanged(JoystickEvents.KeyReleased)
        pass
    def onMoveRight(self, event):
        logging.debug("onMoveRight")
        print("MoveRight")
        self._moveVectorX = 1
        self.saveStartingPosition()
        self._playerSprite.joystickChanged(JoystickEvents.MoveRight)
        pass
    def onMoveLeft(self, event):
        logging.debug("onMoveLeft")
        self._moveVectorX = -1
        self.saveStartingPosition()
        self._playerSprite.joystickChanged(JoystickEvents.MoveLeft)
        print("MoveLeft")
        pass
    def onMoveUp(self, event):
        logging.debug("onMoveUp")
        self._moveVectorY = -1
        self.saveStartingPosition()
        self._playerSprite.joystickChanged(JoystickEvents.MoveUp)
        print("MoveUp")
        pass
    def onMoveDown(self, event):
        logging.debug("onMoveDown")
        self._moveVectorY = 1
        self.saveStartingPosition()
        print("MoveDown")
        self._playerSprite.joystickChanged(JoystickEvents.MoveDown)
        pass
    def onJump(self, event):
        logging.debug("onJump")
        print("Jump")
        self.saveStartingPosition()
        self._playerSprite.joystickChanged(JoystickEvents.JumpButton)
        pass
    def onJumpButtonRelease(self, event):
        logging.debug("onJumpButtonRelease")
        print("Jump release")
        self._playerSprite.joystickChanged(JoystickEvents.JumpButtonReleased)
        pass
    def onKeyStart(self, event):
        logging.debug("onKeyStart")
        print("Start")
        pass
    def onKeyExit(self, event):
        logging.debug("onKeyExit")
        print("Exit")
        self._state.done = True
        pass

    def saveStartingPosition(self):
        """Saves time and position when a move starts."""
        self._moveStartTime = pygame.time.get_ticks()
        self._moveStartPosition = (self._position.posX, self._position.posY)


    def loadMap(self, mapName):
        """Loads the view map and configuration."""
        self._configuration = self._loadConfiguration(mapName)
        
        self._viewModelName = mapName
        self._configure(self._configuration)
        
        pass

    def convertMapPositionToScreenPosition(self, mapPosition):
        """Converts the absolute map position to relative screen position."""
        result = (200,200)
        result = (mapPosition[0] - self._position.posX, mapPosition[1] - self._position.posY)
        return result

    def _initializeSprites(self, spriteConfig):
        """Initializes all sprites from config file."""
        for item in spriteConfig:
            spriteType = item["Type"]
            spritePosition = (item["x"], item["y"])
            spriteInstance = createSpriteInstance(spriteType, spritePosition, self.convertMapPositionToScreenPosition)
            self._allSprites.add(spriteInstance)
            self._movingSprites.add(spriteInstance)
        pass

    def _loadSounds(self, soundConfig):
        self._musicPlayer.loadSounds(soundConfig)

        pass

    def _configurePlayer(self, configuration):
        """Configure the player object."""
        if ConfigKey.PlayerType in configuration:
            playername = configuration[ConfigKey.PlayerType]
            # Creates the sprite instance.
            self._playerSprite = createSpriteInstance(playername, self._screen, self._position, self._mapManager)
            # Perform the specific configuration at the player object.
            self._playerSprite.configure(configuration)
            # Adds the player to the sprite group.
            self._allSprites.add(self._playerSprite)
        pass

    def _configure(self, configuration):
        """Configures the view."""
        logging.debug("execute _configure")
        if configuration:
            if ConfigKey.BackgroundImage in configuration:
                self._backgroundImageFileName = configuration[ConfigKey.BackgroundImage]
            self._mapManager = TileMapManager.TileMapManager(self.viewModelName, self._backgroundImageFileName)
            if ConfigKey.NonSolidTiles in configuration:
                # Loads the list of non solid tiles.
                self._mapManager.nonSolidTiles = configuration[ConfigKey.NonSolidTiles]
            # Loads the sprite class for the player from config file.
            if ConfigKey.PlayerSpriteDefinition in configuration:
                self._configurePlayer(configuration[ConfigKey.PlayerSpriteDefinition])
            
            # Gets the Song list from config and creates a music player
            if ConfigKey.Songs in configuration:
                self._musicPlayer = MusicPlayer(configuration[ConfigKey.Songs])
            else:
                logging.warning("No song files in configuration")
            if ConfigKey.StartPlayerAt in configuration:
                self._position.posX = configuration[ConfigKey.StartPlayerAt]["x"]
                self._position.posY = configuration[ConfigKey.StartPlayerAt]["y"]
            else:
                logging.warn("No player start position configured for this map.")
            if ConfigKey.Sprites in configuration:
                self._initializeSprites(configuration[ConfigKey.Sprites])
            else:
                logging.warn("No sprites configured for this map.")
            
            if ConfigKey.Sounds in configuration:
                self._loadSounds(configuration[ConfigKey.Sounds])
            else:
                logging.warn("No sounds configured for this map.")
        else:
            logging.error("Null configuration.")
        pass

    def runView(self):
        """Runs the view."""
        #self.keyboardJoystickChecker()
        self.handleEvents()
        self.updateSprites()
        self.drawView()
        self.checkClashes()
        self.flipScreen()
        pass

    def updateSprites(self):
        """Calculates the next view x,y position."""
        self._playerSprite.update()    
        self._movingSprites.update()

    def _mouseButtonUp(self, event):
        self._infoText = ""
        pass
    def _mouseButtonDown(self, event):
        self._infoText = "MapPos: {0}, {1}".format(self._position.posX + event.pos[0], self._position.posY + event.pos[1])
        print(self._infoText)
        pass

    def onEvent(self, event):
        """Handle events."""
        if event.type == pygame.QUIT:
            self._state.done = True
        elif event.type == pygame.KEYUP:
            self._keyboardEventHandler.handleEvent(event)
        elif event.type == pygame.KEYDOWN:
            self.onKeyboardEvent(event)
            self._keyboardEventHandler.handleEvent(event)
        elif event.type == UserEvents.EVENT_MUSIC:
            self.onMusicEvent(event)
        elif event.type == UserEvents.EVENT_CHANGEVIEW:
            self.onViewChange(event)
        elif event.type == pygame.JOYAXISMOTION:
            self._joystickEventHandler.handleEvent(event)
        elif event.type == pygame.JOYBUTTONDOWN:
            self._joystickEventHandler.handleEvent(event)
        elif event.type == pygame.JOYBUTTONUP:
            self._joystickEventHandler.handleEvent(event)
        elif event.type == pygame.JOYHATMOTION:
            self._joystickEventHandler.handleEvent(event)
        elif event.type == UserEvents.EVENT_MUSIC_ENDED:
            if self._musicPlayer:
                self._musicPlayer.playNextSong()
        elif event.type == pygame.MOUSEBUTTONUP:
            self._mouseButtonUp(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._mouseButtonDown(event)
        else:
            print ("Unhandled: ", event.type)
            if event.type != 27:
                print (event) 
        pass


    def onKeyboardEvent(self, event):
        """Handle the keyboard events."""
        print("A key was pressed: ", event.key)
        if event.key == pygame.K_q:
            # Q Pressed, quit game
            self._state.done = True
        elif event.key == pygame.K_1:
            self._callback(ViewNames.Level1)
        elif event.key == pygame.K_2:
            self._callback(ViewNames.Level1)
        elif event.key == pygame.K_3:
            self._callback(ViewNames.Level2)
        elif event.key == pygame.K_m:
            self._musicPlayer.stop()

        pass


    def onViewChange(self, event):
        """View is going to be changed."""
        # Todo: Implement change the view.
        pass

    def onMusicEvent(self, event):
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

    

    def drawTiles(self):
        """Draw the tiles to the screen."""
        self._mapManager.drawTiles(self._screen, (self._position.posX, self._position.posY))

    def drawScore(self):
        """Draws the score to the screen."""

        background = self._screen.convert()
        score = "x: {:d} y: {:d}".format(self._position.posX, self._position.posY)
        text = self._font.render(score, True, (255, 0, 0))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)
        self._screen.blit(background, (0,0))
        pass

    def drawInfoText(self):
        background = self._screen.convert()
        score = self._infoText
        text = self._font.render(score, True, (255, 0, 0))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.top = background.get_rect().bottom - 50
        background.blit(text, textpos)
        self._screen.blit(background, (0,0))
        pass

    def checkClashes(self):
        """Checks if sprites collides with player."""
        for sprite in self._movingSprites.sprites():
            if pygame.sprite.collide_mask(self._playerSprite, sprite):
                info = sprite._collideCallback()
                if info.sound:
                    self._musicPlayer.playSoundByName(info.sound)
                    if info.spriteDies and info.parent != None:
                        info.parent.kill()
                    if info.playerDies:
                        logging.debug("The player touched with deadly sprite.")
                        #Todo: Player looses life.
        pass


    def drawView(self):
        """Paint the complete view (screen)."""
        self.drawTiles()
        self.drawSprites()
        self.drawScore()
        self.drawInfoText()
   
    def flipScreen(self):
        """Flip the screen."""
        pygame.display.flip()
        self._state.clock.tick(80)
    
    def drawSprites(self):
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









