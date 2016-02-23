from Utils.ViewPluginBase import ViewPluginBase
from Utils.JumpCalculator import JumpCalculator
import pygame
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.PlayerMoveStateMachine import PlayerMoveState, CheckDirection
from Utils.ViewPointer import ViewPoint
from Utils.gui.TextLabel import TextLabel
import json
import os.path

class JumpMode(object):
    Short = 0
    Long = 1


class ShowJump(ViewPluginBase):
    """Displays the jump curve."""
    def __init__(self):
        super().__init__()
        self._pluginVisible = True
        self._player = None
        self._calculationDirty = True
        self._maxCalculationTime = None
        self._parameters = {}
        self._parameters[JumpMode.Short] = (500, 275, 70)
        self._parameters[JumpMode.Long] = (500, 500, 200)
        self._jumpMode = JumpMode.Short


        self._jumpCalculator = JumpCalculator(0.5, 500, 100)
        self._buttons = pygame.sprite.Group()

        self._xGroup = pygame.sprite.Group()
        self._xButton = TextLabel(770, 20)
        self._xButton.caption = "x"
        self._xButton._onClickHandler = self.onXButtonClick
        self._xGroup.add(self._xButton)

        
        self._vxMinus = TextLabel(620,70)
        self._vxMinus._onClickHandler = self.onVxMinusClick
        self._vxMinus.caption = "-VX"
        self._buttons.add(self._vxMinus)

        self._vxPlus = TextLabel(620,30)
        self._vxPlus._onClickHandler = self.onVxPlusClick
        self._vxPlus.caption = "+VX"
        self._buttons.add(self._vxPlus)

        self._v0Plus = TextLabel(660,30)
        self._v0Plus._onClickHandler = self.onV0PlusClick
        self._v0Plus.caption = "+V0"
        self._buttons.add(self._v0Plus)

        self._v0Minus = TextLabel(660,70)
        self._v0Minus._onClickHandler = self.onV0MinusClick
        self._v0Minus.caption = "-V0"
        self._buttons.add(self._v0Minus)

        self._gravPlus = TextLabel(700,30)
        self._gravPlus._onClickHandler = self.on_gravPlusClick
        self._gravPlus.caption = "+Grav."
        self._buttons.add(self._gravPlus)

        self._gravMinus = TextLabel(700,70)
        self._gravMinus._onClickHandler = self.on_gravMinusClick
        self._gravMinus.caption = "-Grav."
        self._buttons.add(self._gravMinus)

        self._buttonJumpMonde = TextLabel(620,110)
        self._buttonJumpMonde.caption = "Short"
        self._buttonJumpMonde._onClickHandler = self.on_jumpModeButtonClick
        self._buttons.add(self._buttonJumpMonde)

        self._buttonSave = TextLabel(680, 110)
        self._buttonSave.caption = "Save"
        self._buttonSave._onClickHandler = self.onSaveButtonClick
        self._buttons.add(self._buttonSave)

        self._buttonLoad = TextLabel(740, 110)
        self._buttonLoad.caption = "Load" 
        self._buttonLoad._onClickHandler = self.onLoadButtonClick
        self._buttons.add(self._buttonLoad)



        self.TIMEREVENT = pygame.USEREVENT + 6
        pygame.time.set_timer(self.TIMEREVENT, 200)

    def initializePlugin(self, parentView):
        super().initializePlugin(parentView)

        if not self._player:
            self._player = ServiceLocator.getGlobalServiceInstance(ServiceNames.Player)
            self._jumpCalculator.g = self._player.jumpG
            self._jumpCalculator.v0 = self._player.jumpV0
            self._jumpCalculator.vx = self._player.jumpVx
        self.registerEventHandler()


    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.handleOnMouseClick(pos)
            if event.type == self.TIMEREVENT:
                self._calculationDirty = True
        pass

    def handleOnMouseClick(self, position):
        for button in self._buttons:
            if button.rect.collidepoint(position):
                button.onClick()
        for button in self._xGroup:
            if button.rect.collidepoint(position):
                button.onClick()
        pass
        
    

    def drawCurveParametersText(self):
        font = pygame.font.Font(None, 24)
        data = "g: {0} V0: {1} Vx: {2}".format(self._jumpCalculator.g, self._jumpCalculator.v0, self._jumpCalculator.vx)
        text = font.render(data, 1, (1, 1, 1))
        textpos = text.get_rect()
        textpos.left = 570
        textpos.top = 470
        self._screen.blit(text, textpos)

    def getMoveStateVector(self):
        vector = None
        if self._player.moveState in [PlayerMoveState.StandingLeft, PlayerMoveState.MoveLeft]:
            vector = 1
        elif self._player.moveState in [PlayerMoveState.StandingRight, PlayerMoveState.MoveRight]:
            vector = -1
        return vector


    def calculateJumpTime(self, vector):
        """Find barriers on the curve."""
        result = None
        offset = ViewPoint(self._viewPointer.playerPositionX, self._viewPointer.playerPositionY)
        abort = False
        time = 0
        while not abort:
            time += 10
            x = self._jumpCalculator.calcX(time)
            y = self._jumpCalculator.calcY(time)
            position = ViewPoint(offset.left - x * vector, offset.top - y)
            # Check barriers
            if self._player.tilesWatcher.isBarrierOnPosition(position, CheckDirection.Ground):
                screenOffset = self._viewPointer.playerOffset.copy()
                vector = self.getMoveStateVector()
                relativ = (screenOffset.left - x * vector, screenOffset.top - y)


                result = (time, position, relativ)
                abort = True
            if time > 3000:
                result = (3000, None, None)
                abort = True
        return result


    def drawMaxCalculationTimePoint(self):
        if self._maxCalculationTime:

            if self._player.moveState in [PlayerMoveState.StandingLeft, PlayerMoveState.MoveLeft]:
                vector = 1
            elif self._player.moveState in [PlayerMoveState.StandingRight, PlayerMoveState.MoveRight]:
                vector = -1

            if self._maxCalculationTime[2]:
                rect = pygame.Rect(self._maxCalculationTime[2][0], self._maxCalculationTime[2][1], 32, 32)
                pygame.draw.rect(self._screen, (0, 255, 0), rect, 2)



    def drawCurve(self):
        vector = self.getMoveStateVector()

        if vector:
            if self._calculationDirty:
                # Calculate maximum jump time
                self._maxCalculationTime = self.calculateJumpTime(vector)
                self._calculationDirty = False

            offset = self._viewPointer.playerOffset.copy()
            #offset.left += 16
            #offset.top += 16
            start = (offset.left + 16, offset.top + 32)
            for i in range(0, 2500, 100):
                x = self._jumpCalculator.calcX(i)
                y = self._jumpCalculator.calcY(i)
                end = (offset.left - x * vector + 16, offset.top - y + 32)
                color = (255, 1, 1) 
                pygame.draw.line(self._screen, color, start, end)
                start = end
                    

            self._buttons.draw(self._screen)
            self.drawCurveParametersText()
            self.drawMaxCalculationTimePoint()
        pass

    def drawJumpUp(self):
        pass

    def drawPlugin(self):

        if self._pluginVisible:
            if self._player.moveState == PlayerMoveState.Standing:
                self.drawJumpUp()
            self.drawCurve()
        self._xGroup.draw(self._screen)
        

        

    def update(self):
        return super().update()

    def onVxMinusClick(self, sender):
        self._jumpCalculator.vx -= 10
        self._player.jumpVx -=10
        self._calculationDirty = True
        pass

    def onVxPlusClick(self, sender):
        self._jumpCalculator.vx += 10
        self._player.jumpVx += 10
        self._calculationDirty = True

    def onV0PlusClick(self, sender):
        self._jumpCalculator.v0 += 10
        self._player.jumpV0 +=10
        self._calculationDirty = True

    def onV0MinusClick(self, sender):
        self._jumpCalculator.v0 -= 10
        self._player.jumpV0 -= 10
        self._calculationDirty = True

    def on_gravPlusClick(self, sender):
        self._jumpCalculator.g += 10
        self._player.jumpG += 10
        self._calculationDirty = True

    def on_gravMinusClick(self, sender):
        self._jumpCalculator.g -= 10
        self._player.jumpG -= 10
        self._calculationDirty = True

    def on_jumpModeButtonClick(self, sender):
        if self._jumpMode == JumpMode.Short:
            self.jumpMode = JumpMode.Long
        else:
            self.jumpMode = JumpMode.Short
    def onSaveButtonClick(self, sender):
        #Save current jump parameters into parameters store
        self._parameters[self._jumpMode] = (self._jumpCalculator.g, self._jumpCalculator.v0, self._jumpCalculator.vx)
        #Save into file
        with open('jumpdata.json', 'w') as outfile:
            json.dump(self._parameters, outfile)

        pass
    def onLoadButtonClick(self, sender):
        data = None
        if os.path.isfile('jumpdata.json'):
            with open('jumpdata.json') as data_file:
                data = json.load(data_file)
            self._parameters[JumpMode.Short] = data["{0}".format(JumpMode.Short)]
            self._parameters[JumpMode.Long] = data["{0}".format(JumpMode.Long)]
            #Reload
            self.jumpMode = self.jumpMode
        pass

    def onXButtonClick(self, sender):
        """User clicks on x button."""
        if self._pluginVisible:
            self._pluginVisible = False
        else:
            self._pluginVisible = True
        pass

    def changeJumpMode(self, mode):
        parameters = self._parameters[mode]
        self._jumpCalculator.g = parameters[0]
        self._jumpCalculator.v0 = parameters[1]
        self._jumpCalculator.vx = parameters[2]
        if mode == JumpMode.Long:
            self._buttonJumpMonde.caption = "Long"
        else:
            self._buttonJumpMonde.caption = "Short"

    @property
    def jumpMode(self):
        return self._jumpMode
    @jumpMode.setter
    def jumpMode(self, value):
        self._jumpMode = value
        self.changeJumpMode(value)





