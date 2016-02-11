from math import sin, radians
class JumpCalculator(object):
    """description of class"""
    def __init__(self, alpha, v, g):
        self.alpha = alpha
        self.v = v
        self.g = g

    def CalcV(self, time):
        result = self.v * sin(radians(self.alpha)) - self.g * time
        return result


