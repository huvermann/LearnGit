import unittest
from Sprites.SpriteFactory import createSpriteInstance

class Test_SpriteFactoryTests(unittest.TestCase):
    def test_CreateSpriteInstance(self):
        """Tests if createSpriteInstance creates an instance of a class by name and calls the constuctor with parameters."""

        exp1 = "Test1"
        exp2 = "Test2"
        actual = createSpriteInstance("MockSprite", exp1, exp2)
        self.assertIsNotNone(actual)
        self.assertEqual(exp1, actual.param1)
        self.assertEqual(exp2, actual.param2)


if __name__ == '__main__':
    unittest.main()
