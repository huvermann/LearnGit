import importlib

def createObjectInstance(classname):
    module_name = "MapObjects.{0}".format(classname)
    objectClass = getattr(importlib.import_module(module_name), classname)
    return objectClass()




