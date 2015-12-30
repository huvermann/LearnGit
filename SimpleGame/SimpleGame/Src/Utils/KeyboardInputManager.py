import pygame
from Utils.InputManagerBase import InputManagerBase

class KeyboardInputManager(InputManagerBase):
    """Maps the keyboard events to the action calls."""
    def __init__(self, keyRight=None, keyLeft=None, keyUp=None, keyDown=None, keyJump=None, keyStart=None, keyExit=None):
        super().__init__()
        self._keyRight = keyRight
        self._keyLeft = keyLeft
        self._keyUp = keyUp
        self._keyDown = keyDown
        self._keyJump = keyJump
        self._keyStart = keyStart
        self._keyExit = keyExit
        self._keyReleaseButton = 3

    


    def handleEvent(self, event):
        """Handle the keyboard events"""
        print("Keyboard-Handler")
        handled = True
        if event.type == pygame.KEYUP:
            if self.onButtonUp:
                self.onButtonUp(event)
        elif event.key == self._keyRight:
            if self.onMoveRight:
                self.onMoveRight(event)
        elif event.key == self._keyLeft:
            if self.onMoveLeft:
                self.onMoveLeft(event)
        elif event.key == self._keyDown:
            if self.onMoveDown:
                self.onMoveDown(event)
        elif event.key == self._keyUp:
            if self.onMoveUp:
                self.onMoveUp(event)
        elif event.key == self._keyJump:
            if self.onJump:
                self.onJump(event)
        elif event.key == self._keyStart:
            if self.onStart:
                self.onStart(event)
        elif event.key == self._keyExit:
            if self.onExit:
                self.onExit(event)
        else:
            handled = False
        return handled
    @staticmethod
    def default():
        """Returns a instance of the keyboard event handler"""
        return KeyboardInputManager(
            keyRight=pygame.K_RIGHT,
            keyLeft=pygame.K_LEFT,
            keyUp=pygame.K_UP,
            keyDown=pygame.K_DOWN,
            keyJump=pygame.K_SPACE,
            keyExit=pygame.K_ESCAPE,
            keyStart=pygame.K_LCTRL)



