import threading
import time
from gpiozero import PWMOutputDevice

class Servo:

    def __init__(self, pin, pwMin = .0010, pwCtr = .0015, pwMax = .0020, dir = 1):

        self.pin = pin
        self.dir = dir
        self.freq = 200.
        self.pwMin = pwMin
        self.pwMax = pwMax
        self.pwCtr = pwCtr
        self.pwmDev = PWMOutputDevice(self.pin, True, self.dutyCycle(self.pwCtr), self.freq)
        self.pwmDev.value = self.valToDutyCycle(0)
        time.sleep(.25)
        self.pwmDev.off()
        self.currVal = 0
        self.targetVal = 0
        self.tolerance = .005
        self.moveTime = .3 # time to move from value of 0 to 1
        self.moving = False

    def center(self):
        self.move(0)

    def dutyCycle(self, pw):
        return pw * self.freq

    def _move(self):
        deltaVal = self.targetVal - self.currVal
        while abs(deltaVal) > self.tolerance:
            self.moving = True
            timeStep = 1 / self.freq
            valStep = 1 / self.moveTime / self.freq
            if deltaVal > 0:
                self.currVal += valStep
            elif deltaVal < 0:
                self.currVal -= valStep
            self.pwmDev.value = self.valToDutyCycle(self.dir * self.currVal)
            time.sleep(timeStep)
            deltaVal = self.targetVal - self.currVal
        self.moving = False
        self.pwmDev.off()

    def move(self, val):
        self.targetVal = val
        if not self.moving:
            th = threading.Thread(target = self._move, args = [])
            th.start()

    def sweep(self, sweepTime = 3):
        from math import sin, pi
        for step in range(361):
            self.move(sin(2 * pi * step / 360))
            time.sleep(sweepTime / 360.)

    def valToDutyCycle(self, val):
        if val < -1:
            pw = self.pwMin
        elif val < 0:
            pw = abs(val) * self.pwMin + (1 - abs(val)) * self.pwCtr
        elif val > 1:
            pw = self.pwMax
        else:
            pw = abs(val) * self.pwMax + (1 - abs(val)) * self.pwCtr
        return self.dutyCycle(pw)
