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

def getConfigurationFile(viewName):
    '''Returns the configuration file of the view.'''
    return os.path.join(getBasePath(), "Assets", "Views", viewName, "config.json")


def getMapImageResourceFile(viewName):
    '''Returns the tile image map of the view.'''
    return os.path.join(getBasePath(), "Assets", "Views", viewName, viewName + ".png")

def getBackgroundImageResourceFile(viewName):
    '''Returns the background image file of a view.'''
    return os.path.join(getBasePath(), "Assets", "Views", viewName, "background.png")

def getSongResourceFile(filename):
    '''Returns the song filename.'''
    return os.path.join(getBasePath(), "Assets", "Sound", filename)


def getImageResourceFile(resourceName):
    '''Returns an image file path for a resource name.'''
    return os.path.join(getBasePath(), "Assets", "Images", resourceName + ".png")

def getFontResourceFile(fontName):
    '''Gets the font file path of a font.'''
    return os.path.join(getBasePath(), "Assets", "Fonts", fontName + ".ttf")

def getIconResourceFile(resourceName):
    '''Returns the icon resource file path.'''
    return os.path.join(getBasePath(), "Assets", "Images", resourceName + ".ico")




