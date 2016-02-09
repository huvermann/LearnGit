import os
import pygame
from Utils.DirHelper import getSpriteResourceFilename

class AniConfigKeys(object):
    """Contains the animation configuration key strings."""
    Filename = "Filename"
    MaskFilename = "MaskFilename"
    AnimationType = "AnimationType"
    Delay = "Delay"
    StepWith = "StepWith"
    PictureSize = "PictureSize"


class AnimationTypes(object):
    TimeBased = "TimeBased"
    PositionBased = "PositionBased"
    
class AnimationInfo(object):
    """Animation information container"""
    Filename = ""
    MaskFileName = None
    ImageSurface = None
    MaskSurface = None
    ImageCount = None
    ImageRect = None
    AnimationType = None
    Delay = None
    StepWith = None
    PictureSize = None

    def __init__(self, **kwargs):
        return super().__init__(**kwargs)

    def configure(self, spriteName, animationname, configuration):
        #Todo: Implement AnimationInfo.configure(configuration)
        self.Filename = configuration[AniConfigKeys.Filename]
        if AniConfigKeys.MaskFilename in configuration:
            self.MaskFileName = configuration[AniConfigKeys.MaskFilename]
        if AniConfigKeys.AnimationType in configuration:
            self.AnimationType = configuration[AniConfigKeys.AnimationType]
            if self.AnimationType == AnimationTypes.TimeBased:
                self.Delay = configuration[AniConfigKeys.Delay]
            elif self.AnimationType == AnimationTypes.PositionBased:
                self.StepWith = configuration[AniConfigKeys.StepWith]
        else:
            logging.warn("No animationtype configured for animation: {0}".format(animationname))
            self.AnimationType = AnimationTypes.TimeBased
            self.Delay = 200
        #Load the files from folder
        self.ImageSurface = AnimationInfo.loadAnimationResourceFile(spriteName, self.Filename)
        if self.MaskFileName:
            self.MaskSurface = AnimationInfo.loadAnimationResourceFile(spriteName, self.MaskFileName)

        

        # Read ImageRect
        self.ImageRect = self.ImageSurface.get_rect()

        # Calculate ImageCount
        if not self.PictureSize:
            # Assume we have a Squere if no PictureSize is defined.
            self.PictureSize = (self.ImageRect.height, self.ImageRect.height)

        self.ImageCount = self.ImageRect.width // self.PictureSize[0]
        pass

    def getAnimationPictureByIndex(self, index):
        """Returns the surface of the picture by index."""
        # Todo: Implement
        result = None
        left = index * self.PictureSize[0]
        rect = (left, 0, self.PictureSize[0], self.PictureSize[1])
        result = self.ImageSurface.subsurface(rect)
        return result


    @staticmethod
    def loadAnimationResourceFile(spritename, filename):
        result = None
        resourceFile = getSpriteResourceFilename(spritename, filename)
        if os.path.isfile(resourceFile):
            result = pygame.image.load(resourceFile).convert()
        return result



    

