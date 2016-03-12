import importlib
import pygame
import re
from Utils.AnimationInfo import AnimationInfo, MenuAnimationInfo
from Utils.JoystickStates import JoystickEvents
from Utils.UserEvents import EVENT_PLAYSOUND, EVENT_CHANGEVIEW
from Utils.ServiceLocator import ServiceLocator, ServiceNames



class MenueItem():
    def __init__(self, resourceName):
        self.id = None
        self.image = None
        self.TargetView = None
        self.action = None
        self.animation = None
        self._resourceName = resourceName
        self._actionObject = None
        
        

    def configure(self):
        if self.image:
            self.animation = MenuAnimationInfo(self._resourceName, self.image)
    def executeAction(self):
        if self.TargetView:
            changeviewEvent = pygame.event.Event(EVENT_CHANGEVIEW, ViewName=self.TargetView)
            pygame.event.post(changeviewEvent)

        if self.action:
            actionObject = self.actionFactory(self.action)
            actionObject.doAction()

    def actionFactory(self, actionName):
        module_name = "Actions.{0}".format(actionName)
        actionClass = getattr(importlib.import_module(module_name), actionName)
        return actionClass()

class SelectorJoyState():
    WaitForJoyButton = 0
    WaitForReleaseButton = 1
    WaitForReleaseKey = 2

class PlayerMenueSelectorBase(pygame.sprite.Sprite):
    """description of class"""
    def __init__(self):
        self.image = None
        self.rect = None
        self._menuItems = []
        self._resourcePath = None
        self._margin = 0
        self._soundButton = None
        self._soundMove = None
        self._x = None
        self._y = None
        self._itemIndex = 0
        self._joyState = SelectorJoyState.WaitForJoyButton
        self._viewPointer = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewPointer)

        super().__init__()

    def configure(self, config):
        self.configureProperties(config.properties)
        self._x = int(config.x)
        # Tiled workaround: fix y-Axis
        self._y = int(config.y - config.height)

        pass

    def configureProperties(self, properties):
        """Configure the menue from tmx properties."""
        for item in properties:
            if item == 'Margin':
                self._margin=  int(properties[item])
            elif item == 'ResourcePath':
                self._resourcePath = properties[item]
            elif item == 'SoundButton':
                self._soundButton = properties[item]
            elif item == 'SoundMove':
                self._soundMove = properties[item]

        if self._resourcePath:
            for item in properties:
                if item.startswith('MenuItem'):
                    newEntry = self.__parseMenueItemEntry(self._resourcePath, item, properties[item])
                    newEntry.configure()
                    self._menuItems.append(newEntry)

        if 'Pointer' in properties:
             self.pointerImage = MenuAnimationInfo.loadAnimationResourceFile(self._resourcePath, self.parseImagePath(properties['Pointer'])).convert()
             # Make it transparent
             self.pointerImage.set_colorkey(self.pointerImage.get_at((0,0)))
        else:
            raise SystemError("No pointer image defined!")



        self._menuItems.sort(key = lambda item: item.id)
        pass

    def parseImagePath(self, propertyString):
        parts=propertyString.split('=')
        return parts[1]

    def __parseMenueItemEntry(self, resourcePath, item, line):
        result = MenueItem(resourcePath)
        result.id =  int(item.replace('MenuItem', ''))
        commands = line.split(' ')
        for cmd in commands:
            (key, value) = cmd.split('=')
            if key == 'Image':
                result.image = value
            elif key == 'TargetView':
                result.TargetView = value
            elif key == 'Action':
                result.action = value

        return result

    def _playSound(self, soundName):
        print("Playsound: {0}".format(soundName))
        playSoundEvent = pygame.event.Event(EVENT_PLAYSOUND, sound=soundName)
        pygame.event.post(playSoundEvent)
        pass

    def joystickChanged(self, externalInput):
        def waitForJoyButton(input):
            if input == JoystickEvents.MoveDown:
                self.itemIndex += 1
                self.image = None
                if self._soundMove:
                    self._playSound(self._soundMove)
                self._joyState = SelectorJoyState.WaitForReleaseKey


            elif input == JoystickEvents.MoveUp:
                self.itemIndex -= 1
                self.image = None
                if self._soundMove:
                    self._playSound(self._soundMove)

                self._joyState = SelectorJoyState.WaitForReleaseKey
            elif input == JoystickEvents.JumpButton:
                self._joyState = SelectorJoyState.WaitForReleaseButton
                # Execute the action
                self._menuItems[self.itemIndex].executeAction()
                if self._soundButton:
                    #Play the sound
                    self._playSound(self._soundButton)


            pass
        def waitForReleaseButton(input):
            if input == JoystickEvents.JumpButtonReleased:
                self._joyState = SelectorJoyState.WaitForJoyButton
            pass
        def waitForReleaseKey(input):
            if input == JoystickEvents.KeyReleased:
                self._joyState = SelectorJoyState.WaitForJoyButton
            pass

        if self._joyState == SelectorJoyState.WaitForJoyButton:
            waitForJoyButton(externalInput)
        elif self._joyState == SelectorJoyState.WaitForReleaseButton:
            waitForReleaseButton(externalInput)
        elif self._joyState == SelectorJoyState.WaitForReleaseKey:
            waitForReleaseKey(externalInput)
        pass

    def createImage(self):
        result = None
        pointerTop = [0]
        # Calculate Size
        width = 0
        height = 0
        for item in self._menuItems:
            itemRect = item.animation.ImageRect
            if itemRect.width > width:
                width = itemRect.width
            height += itemRect.height + self._margin
            pointerTop.append(height)

        pointerRect = self.pointerImage.get_rect()
        width += self._margin + pointerRect.width
        # Create transparent surface
        if width == 0:
            widt = 1
        if height == 0:
            height = 1
        result = pygame.Surface([width,height])
        result.fill((1,2,3))
        result.set_colorkey(result.get_at((0,0)))

        # Copy items to surface
        y = 0
        menuLeft = pointerRect.width + self._margin
        for item in self._menuItems:
            img = item.animation.ImageSurface
            position = (menuLeft, y)
            result.blit(img, position)
            y += img.get_rect().height + self._margin

        # Paint the pointer:
        result.blit(self.pointerImage, (0, pointerTop[self._itemIndex]))

        # return the surface
        return result



    def update(self, *args):
        """Updates the image."""
        if not self.image:
            self.image = self.createImage()
            self.rect = self.image.get_rect()

        self.rect.left = self._x
        self.rect.top = self._y
        return super().update(*args)

    @property
    def itemIndex(self):
        return self._itemIndex

    @itemIndex.setter
    def itemIndex(self, value):
        max = len(self._menuItems) -1
        if value > max:
            self._itemIndex = 0
        elif value < 0:
            self._itemIndex = max
        else:
            self._itemIndex = value




