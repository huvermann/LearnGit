import os.path, sys
from Utils.Constants import DIRS, FILENAMES

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
    return os.path.join(getBasePath(), DIRS.ASSETS, DIRS.VIEWS, viewName, viewName + ".json")

def getConfigurationFile(viewName):
    '''Returns the configuration file of the view.'''
    return os.path.join(getBasePath(), DIRS.ASSETS, DIRS.VIEWS, viewName, FILENAMES.CONFIG)


def getMapImageResourceFile(viewName):
    '''Returns the tile image map of the view.'''
    return os.path.join(getBasePath(), DIRS.ASSETS, DIRS.VIEWS, viewName, viewName + ".png")

def getBackgroundImageResourceFile(viewName, backgroundfilename):
    '''Returns the background image file of a view.'''
    return os.path.join(getBasePath(), DIRS.ASSETS, DIRS.VIEWS, viewName, backgroundfilename)

def getSongResourceFile(filename):
    '''Returns the song filename.'''
    return os.path.join(getBasePath(), DIRS.ASSETS, DIRS.SOUND, filename)


def getImageResourceFile(resourceName):
    '''Returns an image file path for a resource name.'''
    return os.path.join(getBasePath(), DIRS.ASSETS, DIRS.IMAGES, resourceName + ".png")

def getFontResourceFile(fontName):
    '''Gets the font file path of a font.'''
    return os.path.join(getBasePath(), DIRS.ASSETS, DIRS.FONTS, fontName + ".ttf")

def getIconResourceFile(resourceName):
    '''Returns the icon resource file path.'''
    return os.path.join(getBasePath(), DIRS.ASSETS, DIRS.IMAGES, resourceName + ".ico")

def getSpriteAnimationImage(resourceName, animationName):
    '''Returns a sprite animation image file.'''
    return os.path.join(getBasePath(), DIRS.ASSETS, DIRS.SPRITES, resourceName, resourceName + "_" + animationName + ".png")




