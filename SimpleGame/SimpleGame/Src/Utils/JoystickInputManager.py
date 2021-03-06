import pygame
from Utils.InputManagerBase import InputManagerBase

class ButtonAssignment(object):
    JumpButton = 2
    FireButton = 3
    StartButton = 9
    ExitButton = 8

class JoystickInputManager(InputManagerBase):
    """Maps the joystick events to the action calls"""
    def __init__(self):
        super().__init__()
        self._joystick = self._initJoystick()
        pass

    def _initJoystick(self):
        """Initialize the joystick."""
        joystick = None
        joystickCount = pygame.joystick.get_count()
        if joystickCount == 0:
            print ("No joystick found")
        else:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        return joystick

    def handleEvent(self, event):
        """Handle joystick events."""
        if self._joystick:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == ButtonAssignment.JumpButton:
                    self.onJump(event)
                elif event.button == ButtonAssignment.ExitButton:
                    self.onExit(event)
                elif event.button == ButtonAssignment.StartButton:
                    self.onStart(event)
                else:
                    print(event)

            elif event.type == pygame.JOYBUTTONUP:
                if event.button == ButtonAssignment.JumpButton:
                    self.onJumpButtonRelease(event)

            elif event.type == pygame.JOYHATMOTION:
                x,y = event.value
                if (x == 1):
                    self.onMoveRight(event)
                if (x == -1):
                    self.onMoveLeft(event)
                if y == 1:
                    self.onMoveUp(event)
                if y == -1:
                    self.onMoveDown(event)
                elif y == 0 and x == 0:
                    self.onButtonUp(event)
        pass




