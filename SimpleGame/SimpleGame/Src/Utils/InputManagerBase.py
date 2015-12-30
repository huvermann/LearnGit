class InputManagerBase():
    """Input Manager Base Class to handle input events"""
    def __init__(self):
        self._onMoveRightCallback = None
        self._onMoveLeftCallback = None
        self._onMoveUpCallback = None
        self._onMoveDownCallback = None
        self._onJumpCallback = None
        self._onExitCallback = None
        self._onStartCallback = None
        self._onButtonUpCallback = None
        self._onJumpButtonReleaseCallback = None
        pass

    def __init__(self, moveRight = None, moveLeft = None, moveUp = None, moveDown=None, jump=None, jumpRelease=None, exit=None, start=None, buttonUp=None):
        self._onMoveRightCallback = moveRight
        self._onMoveLeftCallback = moveLeft
        self._onMoveUpCallback = moveUp
        self._onMoveDownCallback = moveDown
        self._onJumpCallback = jump
        self._onExitCallback = exit
        self._onStartCallback = start
        self._onButtonUpCallback = buttonUp
        self._onJumpButtonReleaseCallback = jumpRelease
        pass

    def mapCallbacks(self, onRelease, onRight, onLeft, onUp, onDown, onJump, onJumpRelease, onStart, onExit):
        """Assigns the callbacks."""
        self.onButtonUp = onRelease
        self.onMoveRight = onRight
        self.onMoveLeft = onLeft
        self.onMoveUp = onUp
        self.onMoveDown = onDown
        self.onJump = onJump
        self.onJumpButtonRelease = onJumpRelease
        self.onStart = onStart
        self.onExit = onExit

    def handleEvent(event):
        """Handles the events and calls the callbacks"""
        raise NotImplementedError("This is a base class, please derive from this class.")
        pass

    @property
    def onMoveRight(self):
        return self._onMoveRightCallback
    @onMoveRight.setter
    def onMoveRight(self, value):
        self._onMoveRightCallback = value
        pass

    @property
    def onMoveLeft(self):
        return self._onMoveLeftCallback
    @onMoveLeft.setter
    def onMoveLeft(self, value):
        self._onMoveLeftCallback = value
        pass

    @property
    def onMoveUp(self):
        return self._onMoveUpCallback
    @onMoveUp.setter
    def onMoveUp(self, value):
        self._onMoveUpCallback = value
        pass

    @property
    def onMoveDown(self):
        return self._onMoveDownCallback
    @onMoveDown.setter
    def onMoveDown(self, value):
        self._onMoveDownCallback = value
        pass

    @property
    def onJump(self):
        return self._onJumpCallback
    @onJump.setter
    def onJump(self, value):
        self._onJumpCallback = value
        pass

    @property
    def onExit(self):
        return self._onExitCallback
    @onExit.setter
    def onExit(self, value):
        self._onExitCallback = value
        pass

    @property
    def onStart(self):
        return self._onStartCallback
    @onStart.setter
    def onStart(self, value):
        self._onStartCallback = value
        pass

    @property
    def onButtonUp(self):
        return self._onButtonUpCallback
    @onButtonUp.setter
    def onButtonUp(self, value):
        self._onButtonUpCallback = value
        pass

    @property
    def onJumpButtonRelease(self):
        return self._onJumpButtonReleaseCallback
    @onJumpButtonRelease.setter
    def onJumpButtonRelease(self, value):
        self._onJumpButtonReleaseCallback = value
        pass









