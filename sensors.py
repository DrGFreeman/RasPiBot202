# Sensor classes

class SensCalPoly: # Polynomial calibration curve class

    def __init__(self, id, signalMin, signalMax, *args):
        self.id = id
        self.coeffs = []
        for arg in args:
            self.coeffs.append(arg)
        self.signalMin = signalMin
        self.signalMax = signalMax

    def setCoeffs(self, *args):
        self.coeffs = []
        for arg in args:
            self.coeffs.append(arg)

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def applyCal(self, signal):
        if self.signalMin <= signal and signal <= self.signalMax:
            calSignal = 0
            degree = 0
            for coeff in self.coeffs:
                calSignal += coeff * signal ** degree
                degree += 1
            return calSignal
        else:
            return -1

class ADistSens:

    def __init__(self, id, analog, aPin, calObj):
        self.id = id
        self.analog = analog[aPin]
        self.aPin = aPin
        self.cal = calObj

    def setCal(self, calObj):
        self.cal = calObj

    def getObstDist(self):
        return self.cal.applyCal(self.analog)

    def hasObst(self, distMin, distMax):
        obstDist = self.getObstDist()
        if obstDist != -1 and distMin <= obstDist and obstDist <= distMax:
            return True
        else:
            return False

class DProxSens:

    def __init__(self, id, analog, aPin):
        self.id = id
        self.analog = analog[aPin]
        self.aPin = aPin

    def hasObst(self):
        if self.analog < 1023:
            return True
        else:
            return False
