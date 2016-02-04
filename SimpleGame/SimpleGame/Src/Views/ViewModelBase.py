﻿import pygame
import os.path
from decimal import Decimal
import json
from GameState import GameState
from GameColors import GameColors
from Utils import UserEvents, TileMapManager
from Utils.DirHelper import getFontResourceFile, getConfigurationFile
from pygame.color import THECOLORS
from Utils.KeyboardInputManager import KeyboardInputManager
from Utils.JoystickInputManager import JoystickInputManager
from Utils.MusicPlayer import MusicPlayer
from Utils.Constants import Constants, ViewNames, Corners

from Sprites.SpriteFactory import createSpriteInstance

class ViewModelBase:
    """description of class"""
    def __init__(self, state, screen, changeViewCallback):
        """Inits the view."""
        self._callback = changeViewCallback
        self._state = state
        self._screen = screen
        self.colors = GameColors()
        #self._mapData = None
        self._tileSet = None
        self._mapManager = None
        self._positionX = 0
        self._positionY = 0
        self._moveVectorX = 0
        self._moveVectorY = 0
        self._viewModelName = None
        self._configuration = None
        self._musicPlayer = None
        self._playerSprite = None
        self._moveStartTime = None

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
        self._moveVectorX = 0
        self._moveVectorY = 0
        self.saveStartingPosition()
        pass
    def onMoveRight(self, event):
        self._moveVectorX = 1
        self.saveStartingPosition()
        # print("MoveRight")
        pass
    def onMoveLeft(self, event):
        self._moveVectorX = -1
        self.saveStartingPosition()
        # print("MoveLeft")
        pass
    def onMoveUp(self, event):
        self._moveVectorY = -1
        self.saveStartingPosition()
        print("MoveUp")
        pass
    def onMoveDown(self, event):
        self._moveVectorY = 1
        self.saveStartingPosition()
        print("MoveDown")
        pass
    def onJump(self, event):
        print("Jump")
        self.saveStartingPosition()
        pass
    def onJumpButtonRelease(self, event):
        print("Jump release")
        pass
    def onKeyStart(self, event):
        print("Start")
        pass
    def onKeyExit(self, event):
        print("Exit")
        self._state.done = True
        pass

    def saveStartingPosition(self):
        """Saves time and position when a move starts."""
        self._moveStartTime = pygame.time.get_ticks()
        self._moveStartPosition = (self._positionX, self._positionY)


    def loadMap(self, mapName):
        """Loads the view map and configuration."""
        self._configuration = self._loadConfiguration(mapName)
        self._mapManager = TileMapManager.TileMapManager(mapName)
        self._viewModelName = mapName
        self._configure(self._configuration)
        pass

    def _initializeSprites(self, spriteConfig):
        """Initializes all sprites from config file."""
        for item in spriteConfig:
            spriteType = item["Type"]
            spritePosition = (item["x"], item["y"])
            spriteInstance = createSpriteInstance(spriteType, self._screen, spritePosition)
            self._allSprites.add(spriteInstance)
            self._movingSprites.add(spriteInstance)
        pass

    def _configure(self, configuration):
        """Configures the view."""
        if configuration:
            # Loads the sprite class for the player from config file.
            playername = configuration[Constants.PlayerType]
            if len(playername) > 1:
                # Creates the sprite instance.
                self._playerSprite = createSpriteInstance(playername, self._screen)
                # Adds the player to the sprite group.
                self._allSprites.add(self._playerSprite)
            # Gets the Song list from config and creates a music player
            self._musicPlayer = MusicPlayer(configuration[Constants.Songs])
            if configuration[Constants.StartPlayerAt]:
                self._positionX = configuration[Constants.StartPlayerAt]["x"]
                self._positionY = configuration[Constants.StartPlayerAt]["y"]
            if configuration[Constants.Sprites]:
                self._initializeSprites(configuration[Constants.Sprites])
        pass

    def runView(self):
        """Runs the view."""
        #self.keyboardJoystickChecker()
        self.handleEvents()
        self.calculateMovements()
        self.updateScreen()
        self.flipScreen()
        pass

    def calculateGroundedMove(self, xVector, startTime, startPos, speed, now):
        
        result = self._positionX
        if startTime:
            duration = now - startTime
            move = duration * speed / 1000 * xVector
            result = int(startPos[0] + move)
        return result

    def calculateHorizontalMove(self, yVector, startTime, startPos, speed, now):
        result = self._positionY
        if startTime:
            duration = now - startTime
            move = duration * speed / 1000 * yVector
            result = int(startPos[1] + move)
        return result

    def _playerCanMove(self, xpos, ypos):
        """Checks if player can move to that map position."""
        coord = self._mapManager.getPlayerTileCoordinate(self._screen, (self._positionX, self._positionY))
        tileType = self._mapManager.getTileType(coord[0], coord[1])
        # Todo: Implement to check underlaying tiles.
        return True

    def _playerIsFalling(self, tileInfo):
        """Returns true, if player is not standing on ground"""
        result = (tileInfo[Corners.GroundContact]["index"] == 0)
        return result

    def calculateMovements(self):
        """Calculates the next view x,y position."""

        position = (self._positionX + self._playerSprite.rect.left, self._positionY+ self._playerSprite.rect.top)
        info = self._mapManager.getTouchedTiles(position, self._playerSprite.rect.size)

        if self._playerSprite:
            if self._playerIsFalling(info):
                # Player falls
                self._positionY += 2 # Very simple gravity solution

            elif self._moveStartTime:
                now = pygame.time.get_ticks()
                newX = self._positionX
                newY = self._positionY

                if self._moveVectorX != 0:
                    newX = self.calculateGroundedMove(self._moveVectorX, self._moveStartTime, self._moveStartPosition, self._playerSprite.speed, now)
                if self._moveVectorY != 0:
                    newY = self.calculateHorizontalMove(self._moveVectorY, self._moveStartTime, self._moveStartPosition, self._playerSprite.speed+10, now)

                if self._playerCanMove(newX, newY):
                    self._positionX = newX
                    self._positionY = newY
            #Todo: update with move state
            self._playerSprite.update(self._moveVectorX, self._moveVectorY)

            self._movingSprites.update()


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
        elif event.type == UserEvents.EVENT_NOISE:
            self.onNoiseEvent(event)
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
            self._callback(ViewNames.View1)
        elif event.key == pygame.K_2:
            self._callback(ViewNames.Level1)
        elif event.key == pygame.K_3:
            self._callback(ViewNames.Level2)
        elif event.key == pygame.K_m:
            self._musicPlayer.stop()

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

    def drawTiles(self):
        """Draw the tiles to the screen."""
        self._mapManager.drawTiles(self._screen, (self._positionX, self._positionY))

    def drawScore(self):
        """Draws the score to the screen."""

        background = self._screen.convert()
        score = "x: {:d} y: {:d}".format(self._positionX, self._positionY)
        text = self._font.render(score, True, (255, 0, 0))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)
        self._screen.blit(background, (0,0))
        pass

    
    def updateScreen(self):
        """Paint the screen."""
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









