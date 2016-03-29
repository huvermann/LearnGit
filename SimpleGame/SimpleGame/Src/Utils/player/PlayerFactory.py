import importlib

def createPlayerInstance(playerName, *args):
    module_name = "Players.{0}".format(playerName)
    spriteClass = getattr(importlib.import_module(module_name), playerName)
    return spriteClass(*args)