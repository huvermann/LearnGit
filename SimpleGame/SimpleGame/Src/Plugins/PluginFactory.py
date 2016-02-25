from Plugins.ShowJump import ShowJump
from Plugins.ShowTileNumbers import ShowTileNumbers
from Plugins.CollosionLab import CollosionLab

def createPluginInstance(pluginName):
    pluginType = globals()[pluginName]
    return pluginType()


