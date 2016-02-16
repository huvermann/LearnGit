from Sprites.JimboSprite import JimboSprite
from Sprites.CoinSprite import CoinSprite
from Sprites.BlobSprite import BlobSprite
from Sprites.MockSprite import MockSprite
from Sprites.DrawbridgeSprite import DrawbridgeSprite
from Sprites.HeartSprite import HeartSprite
from Sprites.JohnDoeSprite import JohnDoeSprite


def createSpriteInstance(spriteName, *args):
    spriteType = globals()[spriteName]
    return spriteType(*args)


