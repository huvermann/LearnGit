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
      "Falling": {
        "Filename": "standing_front.png",
        "AnimationType": "TimeBased",
        "ImageCount": 1,
        "Delay": 25
      },
      "Left": {
        "Filename": "walk_left.png",
        "AnimationType": "PositionBased",
        "ImageCount": 9,
        "StepWith": 8
      },
      "Right": {
        "Filename": "walk_right.png",
        "AnimationType": "PositionBased",
        "ImageCount": 9,
        "StepWith": 8
      },
      "JumpLeft": {
        "Filename": "jump_left.png",
        "AnimationType": "TimeBased",
        "ImageCount" :  9,
        "Delay": 25
      },
      "JumpRight": {
        "Filename": "jump_right.png",
        "AnimationType": "TimeBased",
        "ImageCount": 9,
        "Delay": 25
      },
      "JumpUp": {
        "Filename": "jump_up.png",
        "AnimationType": "TimeBased",
        "ImageCount": 10,
        "Delay": 25
      } }'''
        return json.loads(data)
        


