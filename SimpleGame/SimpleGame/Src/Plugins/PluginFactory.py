from Plugins.ShowJump import ShowJump


def createPluginInstance(pluginName):
    pluginType = globals()[pluginName]
    return pluginType()


