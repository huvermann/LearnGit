import pygame
import logging
from Utils.DirHelper import getFontResourceFile
from Utils.KeyboardInputManager import KeyboardInputManager
from Utils.JoystickInputManager import JoystickInputManager
from Utils.JoystickStates import JoystickEvents
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils import UserEvents
from Utils.ViewPointer import ViewPointer, ViewPoint
from MapObjects.BeamPoint import BeamPoint
from Utils.SavePoint import SavePoint


class ViewModelBase2():
    """Viewmodel base class."""

    def __init__(self, viewName):
        """Constructor of the ViewModel base class."""
        self._viewName = viewName
        self._screen = ServiceLocator.getGlobalServiceInstance(ServiceNames.Screen)
        self.__map = None
        self.__mapObjects = []
        self._beamPointRegistry = {}
        self.__drawBackground = None
        self.__drawTilesCall = None
        self.__playerSprite = None
        self.__serviceContainer = None
        self._musicPlayer = None
        self._soundPlayer = None
        self.__plugins = []
        self.__objectSprites = pygame.sprite.Group()
        self.__allSprites = pygame.sprite.Group()
        self.__keyboardEventHandler = self.__initKeyboardManager()
        self.__joystickEventHandler = self.__initJoystickManager()
        self._state = ServiceLocator.getGlobalServiceInstance(ServiceNames.Gamestate)
        self.__eventHandlers = [] # Event handlers for plugins
        self._viewPointer = ViewPointer()
        self._gamePaused = False
        self._lifeLostMessageCallback = None
        ServiceLocator.registerGlobalService(ServiceNames.ViewPointer, self._viewPointer)
        

    def suspendView(self):
        """View goes into suspend mode."""
        self.musicPlayer.stop()
        containerServices = [ServiceNames.CurrentView, ServiceNames.Map, ServiceNames.Player, ServiceNames.ViewPointer]
        container = {}

        for service in containerServices:
            if service in ServiceLocator.services:
                container[service] = ServiceLocator.getGlobalServiceInstance(service)
                ServiceLocator.UnregisterService(service)
        
        self.__serviceContainer = container
        
        pass

    def unSuspendView(self):
        
        if self.__serviceContainer:
            for serviceName in self.__serviceContainer:
                ServiceLocator.registerGlobalService(serviceName, self.__serviceContainer[serviceName])

        pass

    def initializeView(self):
        """View is initialized the first time."""
        # Init MapSize
        self._viewPointer.mapWidth = self.map.width * self.map.tileWidth
        self._viewPointer.mapHeight = self.map.height * self.map.tileHeight

        for obj in self.__mapObjects:
            obj.initializeObject(self)

        # Initialize Plugins
        for plugin in self.plugins:
            plugin.initializePlugin(self)
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
        self._moveStartPosition = (self._viewPointer.playerPositionX, self._viewPointer.playerPositionY)

    def handleEvents(self):
        """Handle all events in event list"""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self._state.done = True
            elif event.type == 4 or event.type == 1:
                pass
            else:
                self.onEvent(event)
        for handler in self.__eventHandlers:
            handler(events)
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
        elif event.type == UserEvents.EVENT_CHANGEVIEW:
            self.onViewChange(event)
        elif event.type == UserEvents.EVENT_NEWGAME:
            self.onNewGameEvent(event)
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
        elif event.type == UserEvents.EVENT_PLAYSOUND:
            self.playSoundEvent(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._mouseButtonUp(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._mouseButtonDown(event)
        #else:
        #    print ("Unhandled: ", event.type)
        #    if event.type != 27:
        #        print (event) 
        pass

    def playSoundEvent(self, event):
        if self.soundPlayer:
            self.soundPlayer.playSoundByName(event.sound)
        pass

    def registerEventHandler(self, handler):
        """To register external event handlers for plugin modules."""
        self.__eventHandlers.append(handler)

    def unRegisterEventHandler(self, handler):
        self.__eventHandlers.remove(handler)
        

    def onKeyboardEvent(self, event):
        """Handle the keyboard events."""
        print("A key was pressed: ", event.key)
        if event.key == pygame.K_q:
            # Q Pressed, quit game
            self._state.done = True
        elif event.key == pygame.K_m:
            self._musicPlayer.stop()

        pass

    def _mouseButtonUp(self, event):
        #self._infoText = ""
        pass
    def _mouseButtonDown(self, event):
        #self._infoText = "MapPos: {0}, {1}".format(self._viewPointer.playerPosition.left + event.pos[0], self._position.posY + event.pos[1])
        #print(self._infoText)
        pass

    def registerSavePoint(self):
        """Saves the current position and camera position."""
        savePoint = SavePoint()
        savePoint.viewName = self.viewName
        savePoint.screenPosition = self._viewPointer.screenPosition.copy()
        savePoint.playerPosition =  ViewPoint(self._viewPointer.playerPositionX, self._viewPointer.playerPositionY)
        ServiceLocator.registerGlobalService(ServiceNames.LastSavePoint, savePoint)
        pass


    def onViewChange(self, event):
        """View is going to be changed."""
        viewController = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewController)
        if 'ViewName' in event.dict:
            if viewController:
                viewController.changeView(event.ViewName)
                if 'Position' in event.dict:
                    viewController.currentView._viewPointer.playerPositionX = event.Position.left
                    viewController.currentView._viewPointer.playerPositionY = event.Position.top
                    viewController.currentView._viewPointer.centerPlayerPositionToScreen(event.Position)
        elif 'SavePoint' in event.dict:
            sp =  event.SavePoint.screenPosition.copy()
            pp = event.SavePoint.playerPosition.copy()
            viewController.currentView._viewPointer.screenPosition = sp
            viewController.currentView._viewPointer.initPlayerPosition(pp.left, pp.top)
            viewController.currentView.player._moveStateMachine.reset()
        pass

    def updateSprites(self):
        """Calculates the next view x,y position."""
        if not self._gamePaused:
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
    
    def drawPlugins(self):
        for plugin in self.__plugins:
            plugin.drawPlugin()

    def drawView(self):
        """Paint the complete view (screen)."""
        self.drawTiles()
        self.drawSprites()
        self.drawPlugins()
        self.drawScore()
        self.drawInfoText()

    def flipScreen(self):
        """Flip the screen."""
        pygame.display.flip()
        self._state.clock.tick(80)

    def restartGame(self):
        """Go to savepoint and resume game."""
        savePoint = ServiceLocator.getGlobalServiceInstance(ServiceNames.LastSavePoint)
        if savePoint:
            assert isinstance(savePoint, SavePoint), "Expected to get a SavePoint type."
            changeviewEvent = pygame.event.Event(UserEvents.EVENT_CHANGEVIEW, SavePoint = savePoint)
        pygame.event.post(changeviewEvent)
        pass

    def gameOver(self):
        """Terminate the game and go to game over view."""
        # Change to gameover view.
        gameOverViewName = ServiceLocator.getGlobalServiceInstance(ServiceNames.GameLostTarget)
        changeviewEvent = pygame.event.Event(UserEvents.EVENT_CHANGEVIEW, ViewName=gameOverViewName)
        pygame.event.post(changeviewEvent)


    def onNewGameEvent(self, event):
        """Game has been lost. Start a new game if still lifes are left. The newgame user event is thrown by the LifeLostMessage."""
        self._gamePaused = False
        if self._state.lifes > 0:
            self.restartGame()
        else:
            self.gameOver()

        pass

    def showLostLiveDialog(self):
        #Todo: implement lost life dialog
        if self.lifeLostMessageCallback:
            self._gamePaused = True
            self.lifeLostMessageCallback(self.allSprites, self.objectSprites)
        pass


    def playerLostHisLive(self):
        """The player has lost a live."""
        self._state.lifes -= 1
        self.showLostLiveDialog()
        self._state.energy = 100


    def checkClashes(self):
        """Checks if sprites collides with player."""
        if not self._gamePaused:
            for sprite in self.__objectSprites:
                if pygame.sprite.collide_mask(self.__playerSprite, sprite):
                    info = sprite.doCollide()
                    if info:
                        self._state.points += info.points
                        self._state.energy += info.energy

                        if info.sound:
                            self.soundPlayer.playSoundByName(info.sound)
                        if info.spriteDies and info.parent != None:
                            info.parent.kill()
                        if info.playerDies:
                            logging.debug("The player touched with deadly sprite.")
                            self.playerLostHisLive()
                        elif self._state.energy <= 0:
                            self.playerLostHisLive()

    def updateCameraPosition(self):
        """Updates the viewPointer camera position."""
        self._viewPointer.updateCamera()

    def runView(self):
        """Runs the view."""
        self.handleEvents()
        self.updateCameraPosition()
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
        ServiceLocator.registerGlobalService(ServiceNames.Map, self.__map)

    @property
    def player(self):
        return self.__playerSprite
    @player.setter
    def player(self, value):
        self.__playerSprite = value
        ServiceLocator.registerGlobalService(ServiceNames.Player, self.__playerSprite)

    @property
    def objectSprites(self):
        return self.__objectSprites

    @property
    def allSprites(self):
        return self.__allSprites

    @property
    def plugins(self):
        return self.__plugins

    @property
    def mapObjects(self):
        return self.__mapObjects

    @property
    def beamPointRegistry(self):
        return self._beamPointRegistry

    @property
    def musicPlayer(self):
        return self._musicPlayer
    @musicPlayer.setter
    def musicPlayer(self, value):
        self._musicPlayer = value

    @property
    def soundPlayer(self):
        return self._soundPlayer

    @soundPlayer.setter
    def soundPlayer(self, value):
        self._soundPlayer = value

    @property
    def lifeLostMessageCallback(self):
        return self._lifeLostMessageCallback

    @lifeLostMessageCallback.setter
    def lifeLostMessageCallback(self, value):
        self._lifeLostMessageCallback = value





