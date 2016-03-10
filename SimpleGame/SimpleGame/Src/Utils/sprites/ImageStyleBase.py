from Utils.sprites.SpriteStyleBase import SpriteStyleBase
from Utils.DirHelper import getSpriteResourceFilename
from Utils.AnimationInfo import AnimationInfo, AnimationTypes
import os
import pygame

class ImageStyleBase(SpriteStyleBase):
    """description of class"""
    def __init__(self, parent, properties):
        #return super().__init__(parent, properties)
        self._transparency = self.getTransparencyFromProperties(properties)
        self._imageFileName = self.getImageNameFromProperties(properties)
        self.image = self.loadImage(parent.name, self._imageFileName, self._transparency)
        
        pass

    def loadImage(self, path, filename, transparency):
        result = None
        resourceFile = getSpriteResourceFilename(path, filename)
        if os.path.isfile(resourceFile):
            result = pygame.image.load(resourceFile).convert()
            if transparency:
                result.set_colorkey(result.get_at((0,0)))
        else:
            raise FileNotFoundError(resourceFile)
        return result

    def getTransparencyFromProperties(self, properties):
        result = True
        if "Transparency" in properties:
            result = properties["Transparency"] in ['True', 'true', 1]
        return result


    def getImageNameFromProperties(self, properties):
        result = None
        if 'Image' in properties:
            result = properties['Image']
        return result

    def getImage(self, sprite, ticks):
        return self.image




