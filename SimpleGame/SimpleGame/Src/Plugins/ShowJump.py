from Utils.ViewPluginBase import ViewPluginBase
from Utils.JumpCalculator import JumpCalculator
import pygame
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.PlayerMoveStateMachine import PlayerMoveState, CheckDirection
from Utils.ViewPointer import ViewPoint
from Utils.gui.TextLabel import TextLabel

class ShowJump(ViewPluginBase):
    """Displays the jump curve."""
    def __init__(self):
        super().__init__()
        self._player = None
        self._calculationDirty = True
        self._maxCalculationTime = None
        self._jumpCalculator=JumpCalculator(0.5, 500, 100)
        self._buttons = pygame.sprite.Group()
        
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

        self.TIMEREVENT = pygame.USEREVENT + 6
        pygame.time.set_timer(self.TIMEREVENT, 200)


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



    def drawPlugin(self):
        if not self._curentView:
            self.registerEventHandler()
        if not self._player:
            self._player = ServiceLocator.getGlobalServiceInstance(ServiceNames.Player)
            self._jumpCalculator.g = self._player.jumpG
            self._jumpCalculator.v0 = self._player.jumpV0
            self._jumpCalculator.vx = self._player.jumpVx

        vector = self.getMoveStateVector()
        #if self._player.moveState in [PlayerMoveState.StandingLeft, PlayerMoveState.MoveLeft]:
        #    vector = 1
        #elif self._player.moveState in [PlayerMoveState.StandingRight, PlayerMoveState.MoveRight]:
        #    vector = -1

        if vector:
            if self._calculationDirty:
                # Calculate maximum jump time
                self._maxCalculationTime = self.calculateJumpTime(vector)
                self._calculationDirty = False

            offset = self._viewPointer.playerOffset.copy()
            offset.left += 16
            offset.top += 16
            start = (offset.left, offset.top)
            for i in range(0, 2500, 100):
                x = self._jumpCalculator.calcX(i)
                y = self._jumpCalculator.calcY(i)
                end = (offset.left-x * vector, offset.top - y)
                if self._player.tilesWatcher.isBarrierOnPosition(ViewPoint(end[0], end[1]), CheckDirection.Ground):
                    color = (255, 1, 1)
                else:
                    color = (0, 0, 255) 
                pygame.draw.line(self._screen, color, start, end)
                start = end

            self._buttons.draw(self._screen)
            self.drawCurveParametersText()
            self.drawMaxCalculationTimePoint()
        

        

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





