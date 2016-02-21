import pygame

class TextLabel(pygame.sprite.Sprite):
    def __init__(self, x, y, caption = ""):
        super().__init__()
        self._x = x
        self._y = y
        self._buttonColor = (0,0,255)
        self._borderColor = (0,0,0)
        self._borderHeight = 4
        self._borderWidth = 4
        self._onClickHandler = None
        self._caption = None
        self.caption = caption

    def onClick(self):
        if self._onClickHandler:
            self._onClickHandler(self)
        pass
    def updateImage(self):
        font = pygame.font.Font(None, 24)
        text = font.render(self._caption, 1, (255, 10, 10))
        textpos = text.get_rect()
        self.image = pygame.Surface([textpos.width+self._borderWidth * 2, textpos.height+self._borderHeight*2])
        self.image.fill(self._buttonColor)
        #self.image.set_colorkey(self._buttonColor)
        textpos.left = self._borderWidth
        textpos.top = self._borderHeight
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


