import os
import pygame
from Utils.DirHelper import getSpriteResourceFilename

class AniConfigKeys(object):
    """Contains the animation configuration key strings."""
    Filename = "Filename"
    AnimationType = "AnimationType"
    Delay = "Delay"
    StepWith = "StepWith"
    PictureSize = "PictureSize"
    ImageCount = "ImageCount"


class AnimationTypes(object):
    TimeBased = "TimeBased"
    PositionBased = "PositionBased"
    VerticalPositionBased = "VerticalPositionBased"
    TerminatedAnimation = "TerminatedAnimation"
    
class AnimationInfo(object):
    """Animation information container"""
    Filename = ""
    ImageSurface = None
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
        # Set transparence
        self.ImageSurface.set_colorkey(self.ImageSurface.get_at((0,0)))

        #if self.MaskFileName:
        #    self.MaskSurface = AnimationInfo.loadAnimationResourceFile(spriteName, self.MaskFileName)
        #self.MaskSurface = pygame.mask.from_surface(self.ImageSurface)

        # Read ImageRect
        self.ImageRect = self.ImageSurface.get_rect()

        # Calculate ImageCount
        if not self.PictureSize:
            # Assume we have a Squere if no PictureSize is defined.
            self.PictureSize = (self.ImageRect.height, self.ImageRect.height)

        if not AniConfigKeys.ImageCount in configuration:
            self.ImageCount = self.ImageRect.width // self.PictureSize[0]
        else:
            self.ImageCount = configuration[AniConfigKeys.ImageCount]
        pass

    def getAnimationPictureByIndex(self, index):
        """Returns the surface of the picture by index."""
        result = None
        left = index * self.PictureSize[0]
        rect = (left, 0, self.PictureSize[0], self.PictureSize[1])
        result = self.ImageSurface.subsurface(rect)
        return result

    def getAnimationTerminated(self, time):
        #Todo: Implement
        #this is a dummy:
        return self.getAnimationPictureByIndex(0)

    def calculateTimeIndex(self, time):
        return (time // (self.Delay * self.ImageCount)) % self.ImageCount

    def calculatePositionIndex(self, position):
        return (position // (self.StepWith * self.ImageCount)) % self.ImageCount


    @staticmethod
    def loadAnimationResourceFile(spritename, filename):
        result = None
        resourceFile = getSpriteResourceFilename(spritename, filename)
        if os.path.isfile(resourceFile):
            result = pygame.image.load(resourceFile).convert()
        else:
            raise FileNotFoundError(resourceFile)
        return result



    

