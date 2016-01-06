from Sprites.JimboSprite import JimboSprite
from Sprites.MockSprite import MockSprite

def createSpriteInstance(spriteName, *args):
    spriteType = globals()[spriteName]
    return spriteType(*args)


