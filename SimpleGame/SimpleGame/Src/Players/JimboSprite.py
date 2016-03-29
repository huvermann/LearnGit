from Utils.player.PlayerBaseClass import PlayerBaseClass
import pygame
import json

class JimboSprite(PlayerBaseClass):
    """Implementation of the Jimbo player behaviour."""
    def __init__(self):
        spriteName = "Jimbo"
        super().__init__(spriteName)
        config = self.makeJimboConfig()
        self.configureAnimations(config)

    def configureProperties(self, properties):
        """Configure special properties."""
        return super().configureProperties(properties)

    def makeJimboConfig(self):
        data = '''{"Standing": {
        "Filename": "Jimbo_standing.png",
        "AnimationType": "TimeBased",
        "Delay": 250,
        "PictureSize": [ 32, 32 ]
      },
      "Falling": {
        "Filename": "Jimbo_Left.png",
        "AnimationType": "TimeBased",
        "ImageCount": 2,
        "Delay": 25
      },
      "Left": {
        "Filename": "Jimbo_Left.png",
        "AnimationType": "PositionBased",
        "ImageCount": 2,
        "StepWith": 8
      },
      "Right": {
        "Filename": "Jimbo_Right.png",
        "AnimationType": "PositionBased",
        "ImageCount": 2,
        "StepWith": 8
      },
      "JumpLeft": {
        "Filename": "Jimbo_jump_left.png",
        "AnimationType": "TimeBased",
        "ImageCount" :  2,
        "Delay": 25
      },
      "JumpRight": {
        "Filename": "Jimbo_jump_right.png",
        "AnimationType": "TimeBased",
        "ImageCount": 2,
        "Delay": 25
      },
      "JumpUp": {
        "Filename": "Jimbo_Left.png",
        "AnimationType": "TimeBased",
        "ImageCount": 2,
        "Delay": 25
      } }'''
        return json.loads(data)
        




