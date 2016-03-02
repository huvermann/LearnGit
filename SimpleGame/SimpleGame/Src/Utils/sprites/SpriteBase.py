import pygame
import importlib
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Tiled.TiledMap import TiledObjectItem

class SpritePropNames():
    Points = "Points"
    Style = "Style"
    KillSprite ="KillSprite"
    KillPlayer = "KillPlayer"
    Behavior = "Behavior"
    Supplies = "Supplies"
    Energy = "Energy"
    Sound = "Sound"
    Intelligence = "Intelligence"


class SpriteBase(pygame.sprite.Sprite):
    """The sprite base class."""

    def __init__(self):
        """Constructor of the sprite base class."""
        super().__init__()
        self._name = None
        self._x = None
        self._y = None
        self._points = 0 # Points the player gets if this item is touched.
        self._energy = 0 # Energy points the player gets if this is touched.
        self._style = None # The animation style
        self._intelligence = None # artificial intelligence to drive this sprite.
        self._killSprite = True # True if this sprite dies if the player touch it
        self._killPlayer = False # True if the player dies on collision.
        self._sound = None # Contains the sound file that is played on collision.
        self._supplies = None # Items the player gets if sprite is touched.
        self._behavior = None # Special coded behavior that is executed if collided with the player sprite.
        self._viewPointer = ServiceLocator.getGlobalServiceInstance(ServiceNames.ViewPointer)
        pass

    def configureSprite(self, properties):
        """Consume the configured properties and assign the sprite behavior."""
        assert isinstance(properties, TiledObjectItem), "Expected properties to be of type TiledObjectItem."
        self._name = properties.name
        self._x = properties.x
        self._y = properties.y
        self.configureFromProperties(properties.properties)
        pass

    def configureFromProperties(self, properties):
        """Configures the sprite from tmx object properties."""
        def strToBool(value):
            return value in ['1', 'true', 'True', 'yes', 'Yes', 'jupp']

        if SpritePropNames.Points in properties:
            self.points = int(properties[SpritePropNames.Points])
        if SpritePropNames.Energy in properties:
            self.energy = int(properties[SpritePropNames.Energy])
        if SpritePropNames.KillSprite in properties:
            self.killSprite = strToBool(properties[SpritePropNames.KillSprite])
        if SpritePropNames.KillPlayer in properties:
            self.killPlayer = strToBool(properties[SpritePropNames.KillPlayer])
        if SpritePropNames.Sound in properties:
            self.sound = properties[SpritePropNames.Sound]
        if SpritePropNames.Style in properties:
            self.style = self.styleFactory(properties[SpritePropNames.Style])
        if SpritePropNames.Behavior in properties:
            self.behavior = self.behaviorFactory(properties[SpritePropNames.Behavior])
        if SpritePropNames.Supplies in properties:
            self.supplies = self.suppliesFactory(properties[SpritePropNames.Supplies])
        if SpritePropNames.Intelligence in properties:
            self.intelligence = self.intelligenceFactory(properties[SpritePropNames.Intelligence])
        pass

    def styleFactory(self, styleClassName):
        """Creates a style class."""
        module_name = "SpriteStyles.{0}".format(styleClassName)
        styleClass = getattr(importlib.import_module(module_name), styleClassName)
        return styleClass(self)

    def behaviorFactory(self, behaviorClassName):
        """Returns a behavior class."""
        module_name = "SpriteBehaviors.{0}".format(behaviorClassName)
        spriteBehaviorClass = getattr(importlib.import_module(module_name), behaviorClassName)
        return spriteBehaviorClass(self)

    def intelligenceFactory(self, intelligenceClassName):
        """Returns a sprite intelligence class."""
        module_name = "SpriteIntelligence.{0}".format(intelligenceClassName)
        spriteIntelligenceClass = getattr(importlib.import_module(module_name), intelligenceClassName)
        return spriteIntelligenceClass(self)


    def suppliesFactory(self, supplyClassName):
        """Returns a sprite supply class."""
        module_name = "SpriteSupplies.{0}".format(supplyClassName)
        spriteSupplyClass = getattr(importlib.import_module(module_name), supplyClassName)
        return spriteSupplyClass(self)

    def doCollide(self):
        """Is called when the player collides with this sprite."""
        return self._collosionInfo
        
    @property
    def name(self):
        """The name of the sprite."""
        return self._name
        
    @name.setter
    def name(self, value):
        self._self._name = value
            
    @property
    def x(self):
        """The x-position of the sprite."""
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
            
    @property
    def y(self):
        """The y-position of the sprite."""
        return self._y

    @property
    def points(self):
        """Points the player gets if this item is touched."""
        return self._points
    @points.setter
    def points(self, value):
        self._points = value

    @property
    def energy(self):
        """Energy points the player gets if this is touched."""
        return self._energy
    @energy.setter
    def energy(self, value):
        self._energy = value

    @property
    def style(self):
        """The animation style."""
        return self._style
    @style.setter
    def style(self, value):
        self._style = value

    @property
    def intelligence(self):
        """artificial intelligence to drive this sprite."""
        return self._intelligence
    @intelligence.setter
    def intelligence(self, value):
        self._intelligence = value

    @property
    def killSprite(self):
        """ True if this sprite dies if the player touch it."""
        return self._killSprite

    @killSprite.setter
    def killSprite(self, value):
        self._killSprite = value

    @property
    def killPlayer(self):
        """True if the player dies on collision."""
        return self._killPlayer
    @killPlayer.setter
    def killPlayer(self, value):
        self._killPlayer = value

    @property
    def sound(self):
        """Contains the sound file that is played on collision."""
        return self._sound
    @sound.setter
    def sound(self, value):
        self._sound = value

    @property
    def supplies(self):
        """ Items the player gets if sprite is touched."""
        return self._supplies
    @supplies.setter
    def supplies(self, value):
        self._supplies = value

    @property
    def behavior(self):
        """Special coded behavior that is executed if collided with the player sprite."""
        return self._behavior
    @behavior.setter
    def behavior(self, value):
        self._behavior = value


         




