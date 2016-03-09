import pygame
import importlib
from Utils.ServiceLocator import ServiceLocator, ServiceNames
from Tiled.TiledMap import TiledObjectItem
from SpriteIntelligence import DefaultSpriteIntelligence
from Utils.CollosionInfo import CollosionInfo
from Utils.ViewPointer import ViewPoint

class SpriteMoveState():
    FallingDown = 1
    Standing = 2
    MoveLeft = 3
    MoveRight = 4

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
    AssetName = "AssetName"


class SpriteBase(pygame.sprite.Sprite):
    """The sprite base class."""

    def __init__(self):
        """Constructor of the sprite base class."""
        super().__init__()
        self._name = None
        self._x = None
        self._y = None
        self._assetName = None # The path name for sprite resources.
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
        self.rect = None
        self._moveState = None
        self._lastCollide = None
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
        if SpritePropNames.AssetName in properties:
            self._assetName = properties[SpritePropNames.AssetName]
        else:
            self._assetName = self.name

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
            self.style = self.styleFactory(properties[SpritePropNames.Style], properties)
        if SpritePropNames.Behavior in properties:
            self.behavior = self.behaviorFactory(properties[SpritePropNames.Behavior], properties)
        if SpritePropNames.Supplies in properties:
            self.supplies = self.suppliesFactory(properties[SpritePropNames.Supplies], properties)
        if SpritePropNames.Intelligence in properties:
            self.intelligence = self.intelligenceFactory(properties[SpritePropNames.Intelligence], properties)
        #else:
        #    if not self.intelligence:
        #        self.intelligence = DefaultSpriteIntelligence(self)

        pass

    def styleFactory(self, styleClassName, properties):
        """Creates a style class."""
        module_name = "SpriteStyles.{0}".format(styleClassName)
        styleClass = getattr(importlib.import_module(module_name), styleClassName)
        return styleClass(self, properties)

    def behaviorFactory(self, behaviorClassName, properties):
        """Returns a behavior class."""
        module_name = "SpriteBehaviors.{0}".format(behaviorClassName)
        spriteBehaviorClass = getattr(importlib.import_module(module_name), behaviorClassName)
        return spriteBehaviorClass(self, properties)

    def intelligenceFactory(self, intelligenceClassName, properties):
        """Returns a sprite intelligence class."""
        module_name = "SpriteIntelligence.{0}".format(intelligenceClassName)
        spriteIntelligenceClass = getattr(importlib.import_module(module_name), intelligenceClassName)
        return spriteIntelligenceClass(self, properties)


    def suppliesFactory(self, supplyClassName, properties):
        """Returns a sprite supply class."""
        module_name = "SpriteSupplies.{0}".format(supplyClassName)
        spriteSupplyClass = getattr(importlib.import_module(module_name), supplyClassName)
        return spriteSupplyClass(self, properties)

    def getCollideInfo(self):
        """Is called when the player collides with this sprite."""
        result = CollosionInfo(spriteDies = self._killSprite, playerDies = self._killPlayer, points = self.points, energy = self._energy, parent = self, sound = self.sound)
        self.behavior.doCollide()
        return result
        pass


    def doCollide(self):
        if not self._lastCollide:
            self._lastCollide = pygame.time.get_ticks()
            return self.getCollideInfo()
        else:
            now = pygame.time.get_ticks()
            if now - self._lastCollide > 300:
                self._lastCollide = now
                return self.getCollideInfo()
            else:
                return None 
       

    def update(self, *args):
        """Updates the sprite."""
        ticks = pygame.time.get_ticks()
        
        self.image = self._style.getImage(self, ticks)
        if not self.rect:
            self.rect = self.image.get_rect()
        self._intelligence.updatePosition(self, ticks)

        super().update(*args)
        
    @property
    def name(self):
        """The name of the sprite."""
        return self._name
        
    @name.setter
    def name(self, value):
        self._name = value
            
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

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def position(self):
        return ViewPoint(self._x, self._y)

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

    @property
    def assetName(self):
        return self._assetName

    @property
    def collideRect(self):
        """Returns the collide rect. Override this property, if the collide rect is different."""
        result = self.rect.copy()
        result.top = 0
        result.left = 0

        return result

    @property
    def moveState(self):
        return self._moveState

    @moveState.setter
    def moveState(self, value):
        if self._moveState != value:
            self._moveState = value
            self._style.setMoveState(value)


         




