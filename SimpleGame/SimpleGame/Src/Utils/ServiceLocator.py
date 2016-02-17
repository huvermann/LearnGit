
class ServiceNames:
    Gamestate = 'gamestate'
    ViewPointer = 'viewPointer'
    Screen = 'screen'
    ViewController = 'ViewController'
    Map = 'Map'
    Player = 'Player'
    TiledWatcher = 'TiledWatcher'


class ServiceLocator(object):
    """The service locator class."""
    services = None

    @staticmethod
    def registerGlobalService(serviceName, serviceInstance):
        """Register a service instance by name."""
        if not ServiceLocator.services:
            ServiceLocator.services={}
        ServiceLocator.services[serviceName] = serviceInstance
        print("Register global Service: {0}".format(serviceName))

    @staticmethod
    def getGlobalServiceInstance(serviceName):
        """Returns the service instance by name."""
        print("Get Global Service Instance: {0}".format(serviceName))
        if serviceName in ServiceLocator.services:
            result = ServiceLocator.services[serviceName]
        else:
            result = None
        return result

    @staticmethod
    def clearGlobalServices():
        """Removes all services from container."""
        ServiceLocator.services.clear()



