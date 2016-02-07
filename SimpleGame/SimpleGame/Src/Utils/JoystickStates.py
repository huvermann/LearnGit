import pygame

class JoystickEvents(object):
    """JoystickState enums"""
    KeyReleased = 0
    MoveRight = 1
    MoveLeft = 2
    MoveUp = 3
    MoveDown = 4
    JumpButton = 5
    JumpButtonReleased = 6

class JoystickState(object):
    """Timebased joystick state class."""
    def __init__(self):
        self._keyState = JoystickEvents.KeyReleased
        self._buttonState = JoystickEvents.JumpButtonReleased
        self._lastKeyChangeTime = None
        self._lastButtonChangeTime = None
        self._onKeyStateChanged = None
        self._onButtonStateChanged = None

    def joystickChanged(self, state):
        if type(state) is  int:
            if state in [JoystickEvents.JumpButton, JoystickEvents.JumpButtonReleased]:
                self.buttonState = state
            elif state in [JoystickEvents.KeyReleased, JoystickEvents.MoveDown, JoystickEvents.MoveLeft, JoystickEvents.MoveRight, JoystickEvents.MoveUp]:
                self.keyState = state
        else:
            raise TypeError("JoystickEvent expected")
    pass

    @property
    def keyState(self):
        return self._keyState

    @keyState.setter
    def keyState(self, value):
        if self._keyState != value:
            self._lastKeyChangeTime = pygame.time.get_ticks()
            self._keyState = value
            if self._onKeyStateChanged:
                self._onKeyStateChanged(value, self._lastKeyChangeTime)

    @property
    def buttonState(self):
        return self._buttonState
    @buttonState.setter
    def buttonState(self, value):
        if self._buttonState != value:
            self._lastButtonChangeTime = pygame.time.get_ticks()
            self._buttonState = value
            if self._onButtonStateChanged:
                self._onButtonStateChanged(value, self._lastButtonChangeTime)

    @property
    def lastChange(self):
        return self._lastKeyChangeTime

    @property
    def lastButtonChange(self):
        return self._lastButtonChangeTime

    @property
    def onKeyStateChanged(self):
        return self._onKeyStateChanged
    @onKeyStateChanged.setter
    def onKeyStateChanged(self, value):
        self._onKeyStateChanged = value

    @property
    def onButtonStateChanged(self):
        return self._onButtonStateChanged
    @onButtonStateChanged.setter
    def onButtonStateChanged(self, value):
        self._onButtonStateChanged = value 


        




