from Sprites.JimboSprite import JimboSprite
from Sprites.CoinSprite import CoinSprite
from Sprites.BlobSprite import BlobSprite
from Sprites.MockSprite import MockSprite

def createSpriteInstance(spriteName, *args):
    spriteType = globals()[spriteName]
    return spriteType(*args)


