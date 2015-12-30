import unittest
from MockHelper.MethodMock import *
from Src.Utils.InputManagerBase import InputManagerBase




class Test_InputManager(unittest.TestCase):
    def setUp(self):
        self.mock = MethodMock()

    def test_CanCreateInputManagerWithoutParameters(self):
        actual = InputManagerBase()
        self.assertIsNotNone(actual)

    def test_CanCreateInputManagerWithParameters(self):
        actual = InputManagerBase(None, None)
        self.assertIsNotNone(actual)

    def test_CreateInputManagerCheckCallbackTwoFields(self):
        actual = InputManagerBase(moveRight=self.mock.method1, moveLeft=self.mock.method2)
        self.assertIsNotNone(actual)
        self.assertEqual(actual.onMoveRight, self.mock.method1)

    def test_CreateInputManagerCheckCallbacksNone(self):
        actual = InputManagerBase()
        self.assertIsNone(actual.onMoveRight, "expected onMoveRight to be None")
        self.assertIsNone(actual.onMoveLeft, "expected onMoveLeft to be None")
        self.assertIsNone(actual.onMoveUp, "expected onMoveUp to be None")
        self.assertIsNone(actual.onMoveDown, "expected onMoveDown to be None")
        self.assertIsNone(actual.onJump, "expected onJump to be None")
        self.assertIsNone(actual.onStart, "expected onStart to be None")
        self.assertIsNone(actual.onExit, "expected onExit to be None")
        pass
    def test_onMoveRightAssigned(self):
        actual = InputManagerBase(self.mock.method1)
        actual.onMoveRight()
        self.assertTrue(self.mock._method1Called)
        self.assertFalse(self.mock._method2Called)
        pass

    def test_onMoveLeftAssigned(self):
        actual = InputManagerBase(moveLeft=self.mock.method2)
        actual.onMoveLeft()
        self.assertFalse(self.mock._method1Called)
        self.assertTrue(self.mock._method2Called)
        pass

    def test_onMoveUpAssigned(self):
        actual = InputManagerBase(moveUp=self.mock.method3)
        actual.onMoveUp()
        self.assertFalse(self.mock._method1Called)
        self.assertTrue(self.mock._method3Called)
        pass

    def test_onMoveDownAssigned(self):
        actual = InputManagerBase(moveDown=self.mock.method3)
        actual.onMoveDown()
        self.assertFalse(self.mock._method1Called)
        self.assertTrue(self.mock._method3Called)
        pass

    def test_onStartAssigned(self):
        actual = InputManagerBase(start=self.mock.method3)
        actual.onStart()
        self.assertFalse(self.mock._method1Called)
        self.assertTrue(self.mock._method3Called)
        pass

    def test_onJumpAssigned(self):
        actual = InputManagerBase(jump=self.mock.method3)
        actual.onJump()
        self.assertFalse(self.mock._method1Called)
        self.assertTrue(self.mock._method3Called)
        pass

    def test_onExitAssigned(self):
        actual = InputManagerBase(exit=self.mock.method3)
        actual.onExit()
        self.assertFalse(self.mock._method1Called)
        self.assertTrue(self.mock._method3Called)
        pass
    
    def test_allCallbacks(self):
        actual = InputManagerBase(self.mock.method1, self.mock.method2, self.mock.method3, self.mock.method4,
                                  self.mock.method5, self.mock.method6, self.mock.method7)
        actual.onMoveRight()
        actual.onMoveLeft()
        actual.onMoveUp()
        actual.onMoveDown()
        actual.onJump()
        actual.onStart()
        actual.onExit()

        self.assertTrue(self.mock._method1Called)
        self.assertTrue(self.mock._method2Called)
        self.assertTrue(self.mock._method3Called)
        self.assertTrue(self.mock._method4Called)
        self.assertTrue(self.mock._method5Called)
        self.assertTrue(self.mock._method6Called)
        self.assertTrue(self.mock._method7Called)



if __name__ == '__main__':
    unittest.main()
