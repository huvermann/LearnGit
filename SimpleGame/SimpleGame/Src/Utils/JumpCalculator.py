class JumpSizeMode():
    Short = 0
    Long = 1

class JumpParameters():
    def __init__(self, **kwargs):
        #return super().__init__(**kwargs)
        self.g = kwargs['g']
        self.v0 = kwargs['v0']
        self.vx = kwargs['vx']
    #    pass

    #g = 0
    #v0 = 0
    #vx = 0

class JumpCalculator(object):
    """Calcualates a ballistic curve."""
    def __init__(self):
        self.g = None #g * 1000 #9.81 #Erdbeschleunigung
        self.v0 = None #v0 # Geschwindigkeit (pixex/s)
        self.vx = None #vx
        self._jumpUpSpeed = 250 / 1000
        self._jumpUpTime = 500 / 1000
        self._fallSpeed = 200 /1000
        self._walkSpeed = 120 / 1000
        self._horizontalJumpSize = None
        self._params = {}
        self._params[JumpSizeMode.Short] = JumpParameters(g=500, v0=275, vx=70)
        self._params[JumpSizeMode.Long] = JumpParameters(g=500, v0=300, vx=100)
        self.horizontalJumpSize = JumpSizeMode.Long


    def calcY(self, time):
        t = time / 1000
        result = int(self.v0 * t - self.g / 2 * t * t)
        return result

    def calcX(self, time):
        result = int(time / 1000 * self.vx)
        return result

    def calcJumpUp(self, time):
        return int(time * self._jumpUpSpeed * -1)

    def calcFalling(self, time):
        return int(time * self._fallSpeed)

    def calcWalking(self, time, vector):
        #Todo Beschleunigung einrechnen
        if time < 300: # Acceleration time.
            speedfactor = time / 300
            result = int(time * self._walkSpeed * speedfactor * vector)
        else:
            result = int(time * self._walkSpeed * vector)
        return result


    @property
    def jumpUpSpeed(self):
        return self._jumpUpSpeed * 1000
    @jumpUpSpeed.setter
    def jumpUpSpeed(self, value):
        self._jumpUpSpeed = value / 1000

    @property
    def jumpUpTime(self):
        return self._jumpUpTime * 1000

    @jumpUpTime.setter
    def jumpUpTime(self, value):
        self._jumpUpTime = value / 1000

    @property
    def fallSpeed(self):
        return self._fallSpeed * 1000
    @fallSpeed.setter
    def fallSpied(self, value):
        self._fallSpeed = value / 1000
    @property
    def walkSpeed(self):
        return self._walkSpeed * 1000

    @walkSpeed.setter
    def walkSpeed(self, value):
        self._walkSpeed = value / 1000
        
    @property
    def horizontalJumpSize(self):
        return self._horizontalJumpSize
    
    @horizontalJumpSize.setter
    def horizontalJumpSize(self, value):
        print("JumpSizeMode: {0}".format(value))
        if value != self._horizontalJumpSize:
            self._horizontalJumpSize = value
            param = self._params[value]
            #Copy the parameters
            self.g = param.g
            self.v0 = param.v0
            self.vx = param.vx
         


        
        
        


