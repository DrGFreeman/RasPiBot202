import numpy as np

class PID:

    def __init__(self, Kp = 1, Ki = 0, Kd = 0):

        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.Kscale = 1
        self.error = 0
        self.errorInt = 0
        self.errorDer = 0
        self.prevError = 0
        self.prevProcVar = 0
        self.prevFiltProcVar = 0
        self.medianFilter = False
        self.derivativeOnPV = False

        
    def getOutput(self, setPoint, procVar, step = 1):

        step = float(step) # Avoid integer division in python 2.7...

        filtProcVar = np.median([self.prevProcVar, procVar])

        if self.medianFilter:

            self.error = setPoint - filtProcVar
            self.errorInt += (self.prevError + self.error) / 2. * step

            if self.derivativeOnPV:
                self.errorDer = (filtProcVar - self.prevFiltProcVar) / step
            else:
                self.errorDer = (self.error - self.prevError) / step          

        else:

            self.error = setPoint - procVar
            self.errorInt += (self.prevError + self.error) / 2. * step

            if self.derivativeOnPV:
                self.errorDer = (ProcVar - self.prevProcVar) / step
            else:
                self.errorDer = (self.error - self.prevError) / step

        self.prevError = self.error
        self.prevProcVar = procVar
        self.prevFiltProcVar = filtProcVar

        return self.Kp * self.error + self.Ki * self.errorInt + self.Kd * self.errorDer
        
    def getError(self):
        return self.error

    def reset(self):
        self.error = 0
        self.errorInt = 0
        self.errorDer = 0
        self.prevError = 0
        self.prevProcVar = 0
        self.prevFiltProcVar = 0

    def setKs(self, Kp, Ki = 0, Kd = 0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def setMedianFilter(self, value):
        self.medianFilter = value

    def setDerivativeOnPV(self, value):
        self.derivativeOnPV = value
