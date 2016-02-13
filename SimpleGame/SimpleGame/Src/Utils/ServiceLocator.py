class ServiceLocator(object):
    """The service locator class."""
    services = None

    @staticmethod
    def registerGlobalService(serviceName, serviceInstance):
        """Register a service instance by name."""
        if not ServiceLocator.services:
            ServiceLocator.services={}
        ServiceLocator.services[serviceName] = serviceInstance

    @staticmethod
    def getGlobalServiceInstance(serviceName):
        """Returns the service instance by name."""
        if serviceName in ServiceLocator.services:
            result = ServiceLocator.services[serviceName]
        else:
            result = None
        return result

    @staticmethod
    def clearGlobalServices():
        """Removes all services from container."""
        ServiceLocator.services.clear()



