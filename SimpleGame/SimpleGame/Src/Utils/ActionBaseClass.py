
def actionFactory(actionClassName):
    """Creates a action class."""
    module_name = "Action.{0}".format(actionClassName)
    styleClass = getattr(importlib.import_module(module_name), actionClassName)
    return styleClass(self, properties)

class ActionBaseClass(object):
    """Implements a container for an action."""
    def doAction(self):
        raise NotImplementedError("This is a base class, don´t call this directly.")




