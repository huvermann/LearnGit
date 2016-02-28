
class ServiceNames:
    PyGame = 'pygame'
    Gamestate = 'gamestate'
    ViewPointer = 'viewPointer'
    Screen = 'screen'
    ViewController = 'viewcontroller'
    Map = 'Map'
    Player = 'Player'
    CurrentView = 'CurrentView'


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

    @staticmethod
    def UnregisterService(serviceName):
        """Unregister service from service list."""
        del(ServiceLocator.services[serviceName])



