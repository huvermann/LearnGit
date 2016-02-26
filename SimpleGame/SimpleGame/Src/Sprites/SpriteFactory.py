import importlib

def createSpriteInstance(spriteName, *args):
    module_name = "Sprites.{0}".format(spriteName)
    spriteClass = getattr(importlib.import_module(module_name), spriteName)
    return spriteClass(*args)



