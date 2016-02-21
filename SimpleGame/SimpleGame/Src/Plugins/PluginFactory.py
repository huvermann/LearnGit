from Plugins.ShowJump import ShowJump
from Plugins.ShowTileNumbers import ShowTileNumbers


def createPluginInstance(pluginName):
    pluginType = globals()[pluginName]
    return pluginType()


