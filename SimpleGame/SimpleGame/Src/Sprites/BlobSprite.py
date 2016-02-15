import pygame
from Utils.SpriteItemBase import SpriteItemBase
from Sprites.MagicSpriteStrings import SpriteNames
from Utils.Constants import SoundNames

class BlobNames(object):
    Left = "links_und_mitte"
    Right = "rechts_und_mitte"
    Die = "sterben"
    Jump = "springen"

class BlobSprite(SpriteItemBase):
    """Implementation of the Blob sprite."""
    def __init__(self):
        spritename = SpriteNames.Bloob
        super().__init__(spritename)
        self._animation = None
        self.rect.left = 100
        self.loadAnimations()
        self._currentAnimation = self._animation[BlobNames.Jump]
        self._collosionInfo.sound = SoundNames.BloobTouched
        pass

    def loadAnimationInfo(self, animationName):
        result = {}
        result["Image"] = SpriteItemBase.loadAnimationFile(self._spriteName, animationName)
        result["Count"] = SpriteItemBase.countAnimationLength(result["Image"])
        result["ImageSize"] = SpriteItemBase.getPictureSize(result["Image"])
        # Set transparence
        result["Image"].set_colorkey(result["Image"].get_at((0,0)))
        return result

    def loadAnimations(self):
        self._animation = {}
        self._animation[BlobNames.Left] = self.loadAnimationInfo(BlobNames.Left)
        self._animation[BlobNames.Right] = self.loadAnimationInfo(BlobNames.Right)
        self._animation[BlobNames.Die] = self.loadAnimationInfo(BlobNames.Die)
        self._animation[BlobNames.Jump] = self.loadAnimationInfo(BlobNames.Jump)

    def update(self):
        """Update the blob sprite."""
        rect = SpriteItemBase.getRectTimeBased(self._currentAnimation["Count"], self._currentAnimation["ImageSize"], 100)
        self.image = self._currentAnimation["Image"].subsurface(rect)
        return super().update()
        pass






