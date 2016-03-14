class FontProperties(object):
    """description of class"""
    FontName = None
    Size = None
    Color = None
    Background = None
    def __init__(self, fontName=None, size=48, color = (0,0,0), background=None):
        self.FontName = fontName
        self.Size = size
        self.Color = color
        self.Background = background
        


