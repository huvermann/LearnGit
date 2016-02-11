class JumpCalculator(object):
    """Calcualates a ballistic curve."""
    def __init__(self, g, v0, vx):
        #super().__init__(**kwargs)
        self.g = g * 1000 #9.81 #Erdbeschleunigung
        self.v0 = v0 # Geschwindigkeit (pixex/s)
        self.vx = vx

    def calcY(self, time):
        t = time / 1000
        result = int(self.v0 * t - self.g / 2 * t * t)
        return result

    def calcX(self, time):
        result = int(time / 1000 * self.vx)
        return result


