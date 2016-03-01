class BeamPointRegistry(object):
    """description of class"""
    def __init__(self):
        self._beamPoints = {}

    def registerBeamPoint(self, beamPoint):
        name = beamPoint.name
        self._beamPoints[name] = beamPoint

    def getBeamPoint(self, pointName):
        return self._beamPoints[pointName]

    def beam(self, pointName):
        point = self._beamPoints[pointName]
        point.beam()


