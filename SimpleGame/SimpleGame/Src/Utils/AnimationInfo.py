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

    

