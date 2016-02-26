from Plugins.ShowJump import ShowJump
from Plugins.ShowTileNumbers import ShowTileNumbers
from Plugins.CollosionLab import CollosionLab
from Plugins.CheatKeyPlugin import CheatKeyPlugin

def createPluginInstance(pluginName):
    pluginType = globals()[pluginName]
    return pluginType()


