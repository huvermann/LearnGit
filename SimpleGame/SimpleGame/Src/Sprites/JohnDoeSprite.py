from Utils.PlayerBaseClass import PlayerBaseClass
import pygame
import json

class JohnDoeSprite(PlayerBaseClass):
    """description of John Doe player behaviour"""
    def __init__(self):
        spriteName = "John_Doe"
        super().__init__(spriteName)
        config = self.makeJohnConfig()
        self.configureAnimations(config)

    def configureProperties(self, properties):
        """Configure special properties."""
        return super().configureProperties(properties)

    def makeJohnConfig(self):
        data = '''{"Standing": {
        "Filename": "standing_front.png",
        "AnimationType": "TimeBased",
        "Delay": 250,
        "PictureSize": [ 32, 32 ]
      },

      "StandingLeft": {
        "Filename": "standing_left.png",
        "AnimationType": "TimeBased",
        "Delay": 250,
        "PictureSize": [ 32, 32 ]
      },

      "StandingRight": {
        "Filename": "standing_right.png",
        "AnimationType": "TimeBased",
        "Delay": 250,
        "PictureSize": [ 32, 32 ]
      },

      "Falling": {
        "Filename": "standing_front.png",
        "AnimationType": "TimeBased",
        "Delay": 25
      },

      "FallingLeft": {
        "Filename": "standing_left.png",
        "AnimationType": "TimeBased",
        "Delay": 25
      },

      "FallingRight": {
        "Filename": "standing_right.png",
        "AnimationType": "TimeBased",
        "Delay": 25
      },

      "Left": {
        "Filename": "walk_left.png",
        "AnimationType": "PositionBased",
        "StepWith": 1
      },
      "Right": {
        "Filename": "walk_right.png",
        "AnimationType": "PositionBased",
        "StepWith": 1
      },
      "JumpLeft": {
        "Filename": "jump_left.png",
        "AnimationType": "TimeBased",
        "Delay": 25
      },
      "JumpRight": {
        "Filename": "jump_right.png",
        "AnimationType": "TimeBased",
        "Delay": 25
      },
      "JumpUp": {
        "Filename": "jump_up.png",
        "AnimationType": "TimeBased",
        "Delay": 25
      },
     "Climb": {
        "Filename": "standing_front.png",
        "AnimationType": "TimeBased",
        "Delay": 25
      } }'''
        return json.loads(data)

    @property
    def collideRect(self):
        """Overwrite collision rectangle: Make it smaller."""
        rect = self.rect.copy()
        rect.top = 0
        rect.left = 9
        rect.width = 14
        return rect

        


