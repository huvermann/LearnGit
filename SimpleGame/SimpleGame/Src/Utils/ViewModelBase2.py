import pygame
import logging
from Utils.DirHelper import getFontResourceFile
from Utils.KeyboardInputManager import KeyboardInputManager
from Utils.JoystickInputManager import JoystickInputManager
from Utils.JoystickStates import JoystickEvents
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils import UserEvents
from Utils.ViewPointer import ViewPointer

class ViewModelBase2():
    """Viewmodel base class."""

    def __init__(self, viewName, screen):
        """Constructor of the ViewModel base class."""
        self._viewName = viewName
        self._screen = screen
        self.__map = None
        self.__drawBackground = None
        self.__drawTilesCall = None
        self.__tileCollider = None
        self.__playerSprite = None
        self.__objectSprites = pygame.sprite.Group()
        self.__allSprites = pygame.sprite.Group()
        self.__initFont()
        self.__keyboardEventHandler = self.__initKeyboardManager()
        self.__joystickEventHandler = self.__initJoystickManager()
        self._state = ServiceLocator.getGlobalServiceInstance("gamestate")
        self._viewPointer = ViewPointer(self.screen.get_rect(), None, None, 228+400, 87+250)
        ServiceLocator.registerGlobalService(ServiceNames.ViewPointer, self._viewPointer)
      

    def __initFont(self):
        """Inits the default font."""
        fontFile = getFontResourceFile("InknutAntiqua-Light")
        self._font = pygame.font.Font(fontFile, 12)
    pass

    def __initKeyboardManager(self):
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

    def __initJoystickManager(self):
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
        self.__playerSprite.joystickChanged(JoystickEvents.KeyReleased)
        pass
    def onMoveRight(self, event):
        logging.debug("onMoveRight")
        print("MoveRight")
        self._moveVectorX = 1
        self.saveStartingPosition()
        self.__playerSprite.joystickChanged(JoystickEvents.MoveRight)
        pass
    def onMoveLeft(self, event):
        logging.debug("onMoveLeft")
        self._moveVectorX = -1
        self.saveStartingPosition()
        self.__playerSprite.joystickChanged(JoystickEvents.MoveLeft)
        print("MoveLeft")
        pass
    def onMoveUp(self, event):
        logging.debug("onMoveUp")
        self._moveVectorY = -1
        self.saveStartingPosition()
        self.__playerSprite.joystickChanged(JoystickEvents.MoveUp)
        print("MoveUp")
        pass
    def onMoveDown(self, event):
        logging.debug("onMoveDown")
        self._moveVectorY = 1
        self.saveStartingPosition()
        print("MoveDown")
        self.__playerSprite.joystickChanged(JoystickEvents.MoveDown)
        pass
    def onJump(self, event):
        logging.debug("onJump")
        print("Jump")
        self.saveStartingPosition()
        self.__playerSprite.joystickChanged(JoystickEvents.JumpButton)
        pass
    def onJumpButtonRelease(self, event):
        logging.debug("onJumpButtonRelease")
        print("Jump release")
        self.__playerSprite.joystickChanged(JoystickEvents.JumpButtonReleased)
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
        #self._moveStartPosition = (self._position.left, self._position.top)
        self._moveStartPosition = (self._viewPointer.playerPosition.left, self._viewPointer.playerPosition.top)

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

    def onEvent(self, event):
        """Handle events."""
        if event.type == pygame.QUIT:
            self._state.done = True
        elif event.type == pygame.KEYUP:
            self.__keyboardEventHandler.handleEvent(event)
        elif event.type == pygame.KEYDOWN:
            self.onKeyboardEvent(event)
            self.__keyboardEventHandler.handleEvent(event)
        elif event.type == UserEvents.EVENT_MUSIC:
            self.onMusicEvent(event)
        elif event.type == UserEvents.EVENT_CHANGEVIEW:
            self.onViewChange(event)
        elif event.type == UserEvents.EVENT_NOISE:
            self.onNoiseEvent(event)
        elif event.type == pygame.JOYAXISMOTION:
            self.__joystickEventHandler.handleEvent(event)
        elif event.type == pygame.JOYBUTTONDOWN:
            self.__joystickEventHandler.handleEvent(event)
        elif event.type == pygame.JOYBUTTONUP:
            self.__joystickEventHandler.handleEvent(event)
        elif event.type == pygame.JOYHATMOTION:
            self.__joystickEventHandler.handleEvent(event)
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

    def onNoiseEvent(self, event):
        """Start a sound."""
        # Todo: implement play sound.
        pass


    def updateSprites(self):
        """Calculates the next view x,y position."""
        self.__playerSprite.update()    
        self.objectSprites.update()

    def drawTiles(self):
        """Draw the tiles to the screen."""
        if self._drawBackground:
            self._drawBackground(self.screen, self.map, self._viewPointer)
        if self._drawTilesCall:
            self._drawTilesCall(self.screen, self.map, self._viewPointer)
        else:
            raise NotImplementedError("Please implement drawTiles in your view model.")

    def drawSprites(self):
        "Draws a info text on the screen."
        self.allSprites.draw(self._screen)

    def drawScore(self):
        raise NotImplementedError("Please implement drawScore in your view model.")

    def drawInfoText(self):
        raise NotImplementedError("Please implement drawInfoText in your view model.") 

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

    def checkClashes(self):
        """Checks if sprites collides with player."""
        raise NotImplementedError("Please implement checkClashes in your view model.")



    def runView(self):
        """Runs the view."""
        self.handleEvents()
        self.updateSprites()
        self.drawView()
        self.checkClashes()
        self.flipScreen()
        pass

    @property
    def screen(self):
        return self._screen
    @screen.setter
    def screen(self, value):
        self._screen = value

    @property
    def viewName(self):
        return self._viewName
    @viewName.setter
    def viewName(self, value):
        self.__viewName = value

    @property
    def map(self):
        return self.__map
    @map.setter
    def map(self, value):
        self.__map = value

    @property
    def player(self):
        return self.__playerSprite
    @player.setter
    def player(self, value):
        self.__playerSprite = value

    @property
    def objectSprites(self):
        return self.__objectSprites

    @property
    def allSprites(self):
        return self.__allSprites



