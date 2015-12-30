import pygame
from Utils.InputManagerBase import InputManagerBase

class JoystickInputManager(InputManagerBase):
    """Maps the joystick events to the action calls"""
    def __init__(self):
        super().__init__()
        self._joystick = self._initJoystick()
        pass

    def _initJoystick(self):
        joystick = None
        joystickCount = pygame.joystick.get_count()
        if joystickCount == 0:
            print ("No joystick found")
        else:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        return joystick

    def handleEvent(self, event):
        if self._joystick:
            if event.type == pygame.JOYBUTTONDOWN:
                # Check the Buttons
                if event.button == 1:
                    self.onMoveRight(event)
                elif event.button == 3:
                    self.onMoveLeft(event)
                elif event.button == 0:
                    self.onMoveUp(event)
                elif event.button == 2:
                    self.onMoveDown(event)
                elif event.button == 8:
                    self.onExit(event)
                elif event.button == 9:
                    self.onStart(event)
                else:
                    print(event)

            elif event.type == pygame.JOYBUTTONUP:
                self.onButtonUp(event)
            elif event.type == pygame.JOYHATMOTION:
                x,y = event.value
                if y == 1 and x == 0:
                    self.onJump(event)
                elif y == 0 and x == 0:
                    self.onJumpButtonRelease(event)


        pass




