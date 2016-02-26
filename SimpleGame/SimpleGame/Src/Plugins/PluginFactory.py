import importlib

def createPluginInstance(pluginName):
    module_name = "Plugins.{0}".format(pluginName)
    myClass = getattr(importlib.import_module(module_name), pluginName)
    return myClass()



