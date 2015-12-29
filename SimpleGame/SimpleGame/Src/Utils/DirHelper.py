import os.path, sys

def isRunningInBundle():
    '''Checks if application is running in bundle'''
    if getattr( sys, 'frozen', False ) :
            return True
    else :
        return False

def getBasePath():
    '''Gets the resouceBasePath '''
    if isRunningInBundle():
        return sys._MEIPASS
    else:
        return os.getcwd()

def getMapResourceFile(viewName):
    '''Returns the tile map file of the view.'''
    return os.path.join(getBasePath(), "Assets", "Views", viewName, viewName + ".json")

def getMapImageResourceFile(viewName):
    '''Returns the tile image map of the view.'''
    return os.path.join(getBasePath(), "Assets", "Views", viewName, viewName + ".png")

def getMapSongResourceFile(viewName):
    '''Returns the song file of the view.'''
    raise NotImplementedError()

def getImageResourceFile(resourceName):
    '''Returns an image file path for a resource name.'''
    return os.path.join(getBasePath(), "Assets", "Images", resourceName + ".png")

def getFontResourceFile(fontName):
    '''Gets the font file path of a font.'''
    return os.path.join(getBasePath(), "Assets", "Fonts", fontName + ".ttf")

def getIconResourceFile(resourceName):
    '''Returns the icon resource file path.'''
    return os.path.join(getBasePath(), "Assets", "Images", resourceName + ".ico")




