from Utils.SpriteItemWalkingBase import SpriteItemWalkingBase
from Sprites.MagicSpriteStrings import SpriteNames

class Blob2Sprite(SpriteItemWalkingBase):
    """The 2nd and animated version of the blob sprite."""
    def __init__(self):
        super().__init__(SpriteNames.Bloob)
        self.configureBlobAnimations()

    def configureBlobAnimations(self):
        config = {
            'Left': {'Filename': 'Bloob_gehen_links.png', 'AnimationType': 'PositionBased', 'StepWith': 4},
            'Right': {'Filename': 'Bloob_gehen_rechts.png', 'AnimationType': 'PositionBased', 'StepWith': 8}
            }
        self.configureAnimations(config)
        pass




