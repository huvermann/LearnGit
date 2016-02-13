class ScreenMock(object):
    """Mocks a Screen class."""
    def __init__(self):
        pass

    def blit(self, image, position):
        self.image = image
        self.positon = position





