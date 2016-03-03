class SpriteBehaviorBase(object):
    """description of class"""
    def __init__(self, parent, properties):
        self._parent = parent
        self.configureProperties(properties)

    def configureProperties(self, properties):
        """Configure the properties from the tmx map file."""

        pass

    def doCollide(self):
        """The player collided with this sprite. Override this method."""
        raise NotImplementedError("This is the abstract class. Please implement your behaviour!")


