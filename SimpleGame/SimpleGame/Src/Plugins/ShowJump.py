from Utils.ViewPluginBase import ViewPluginBase
from Utils.JumpCalculator import JumpCalculator
import pygame
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Utils.PlayerMoveStateMachine import PlayerMoveState

class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([32,32])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self._x = x
        self._y = y
        self.rect.top = y
        self.rect.left = x
        self._onClickHandler = None
        self._caption = None
        self.caption = "Hallo"

    def onClick(self):
        if self._onClickHandler:
            self._onClickHandler(self)
        pass
    def updateImage(self):
        font = pygame.font.Font(None, 24)
        text = font.render(self._caption, 1, (255, 10, 10))
        textpos = text.get_rect()
        self.image = pygame.Surface([textpos.width, textpos.height])
        self.image.set_colorkey((0,0,0))
        self.image.blit(text, textpos)
        self.rect = self.image.get_rect()
        self.rect.left = self._x
        self.rect.top = self._y

    @property
    def caption(self):
        return self._caption
    @caption.setter
    def caption(self, value):
        self._caption = value
        self.updateImage()




class ShowJump(ViewPluginBase):
    """Displays the jump curve."""
    def __init__(self):
        super().__init__()
        self._curentView = None
        self._player = None
        g = 0.5
        v0=500
        vx=100
        self._jumpCalculator=JumpCalculator(g, v0, vx)
        self._buttons = pygame.sprite.Group()
        
        self._vxMinus = ButtonSprite(200,70)
        self._vxMinus._onClickHandler = self.onVxMinusClick
        self._vxMinus.caption = "-VX"
        self._buttons.add(self._vxMinus)

        self._vxPlus = ButtonSprite(200,30)
        self._vxPlus._onClickHandler = self.onVxPlusClick
        self._vxPlus.caption = "+VX"
        self._buttons.add(self._vxPlus)

        self._v0Plus = ButtonSprite(240,30)
        self._v0Plus._onClickHandler = self.onV0PlusClick
        self._v0Plus.caption = "+V0"
        self._buttons.add(self._v0Plus)

        self._v0Minus = ButtonSprite(240,70)
        self._v0Minus._onClickHandler = self.onV0MinusClick
        self._v0Minus.caption = "+V0"
        self._buttons.add(self._v0Minus)

        self._gravPlus = ButtonSprite(280,30)
        self._gravPlus._onClickHandler = self.on_gravPlusClick
        self._gravPlus.caption = "+Grav."
        self._buttons.add(self._gravPlus)

        self._gravMinus = ButtonSprite(280,70)
        self._gravMinus._onClickHandler = self.on_gravMinusClick
        self._gravMinus.caption = "-Grav."
        self._buttons.add(self._gravMinus)

        self._timeMinus = ButtonSprite(340,70)
        self._timeMinus._onClickHandler = self.on_TimeMinusClick
        self._timeMinus.caption = "-Time."
        self._buttons.add(self._timeMinus)

        self._timePlus = ButtonSprite(340,30)
        self._timePlus._onClickHandler = self.on_TimePlusClick
        self._timePlus.caption = "+Time."
        self._buttons.add(self._timePlus)

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.handleOnMouseClick(pos)
        pass

    def handleOnMouseClick(self, position):
        for button in self._buttons:
            if button.rect.collidepoint(position):
                button.onClick()
        pass
        
    def registerEventHandler(self):
        # Todo: Implement plugin register mechanism.
        self._curentView = ServiceLocator.getGlobalServiceInstance(ServiceNames.CurrentView)
        if self._curentView:
            self._curentView.registerEventHandler(self.handleEvents)

    def drawCurveParametersText(self):
        font = pygame.font.Font(None, 24)
        data = "g: {0} V0: {1} Vx: {2}, Time: {3}".format(self._jumpCalculator.g, self._jumpCalculator.v0, self._jumpCalculator.vx, self._player.jumpTime)
        text = font.render(data, 1, (1, 1, 1))
        textpos = text.get_rect()
        textpos.left = 570
        textpos.top = 470
        self._screen.blit(text, textpos)



    def drawPlugin(self):
        if not self._curentView:
            self.registerEventHandler()
        if not self._player:
            self._player = ServiceLocator.getGlobalServiceInstance(ServiceNames.Player)
            self._jumpCalculator.g = self._player.jumpG
            self._jumpCalculator.v0 = self._player.jumpV0
            self._jumpCalculator.vx = self._player.jumpVx


        vector = None
        if self._player.moveState in [PlayerMoveState.StandingLeft, PlayerMoveState.MoveLeft]:
            vector = 1
        elif self._player.moveState in [PlayerMoveState.StandingRight, PlayerMoveState.MoveRight]:
            vector = -1

        if vector:
            offset = self._viewPointer.playerOffset.copy()
            offset.left += 16
            offset.top += 16
            start = (offset.left, offset.top)
            for i in range(0, 2500, 100):
                x = self._jumpCalculator.calcX(i)
                y = self._jumpCalculator.calcY(i)
                end = (offset.left-x * vector, offset.top - y)
                pygame.draw.line(self._screen, (255,1,1), start, end)
                start = end

        
            #make point at jump timeout
            pos = (offset.left - self._jumpCalculator.calcX(self._player.jumpTime) * vector, offset.top - self._jumpCalculator.calcY(self._player.jumpTime))
            pygame.draw.circle(self._screen, (255,0,0), pos, 5, 1)
            self._buttons.draw(self._screen)
            self.drawCurveParametersText()
        

        

    def update(self):
        return super().update()

    def onVxMinusClick(self, sender):
        self._jumpCalculator.vx -= 10
        self._player.jumpVx -=10
        pass

    def onVxPlusClick(self, sender):
        self._jumpCalculator.vx += 10
        self._player.jumpVx += 10

    def onV0PlusClick(self, sender):
        self._jumpCalculator.v0 += 10
        self._player.jumpV0 +=10

    def onV0MinusClick(self, sender):
        self._jumpCalculator.v0 -= 10
        self._player.jumpV0 -= 10

    def on_gravPlusClick(self, sender):
        self._jumpCalculator.g += 10
        self._player.jumpG += 10

    def on_gravMinusClick(self, sender):
        self._jumpCalculator.g -= 10
        self._player.jumpG -= 10

    def on_TimeMinusClick(self, sender):
        self._player.jumpTime -= 10
        pass
    def on_TimePlusClick(self, sender):
        self._player.jumpTime += 10
        pass



