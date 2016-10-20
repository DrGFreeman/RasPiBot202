# -*- coding: utf-8 -*-
import threading
import time

from a_star import AStar

# Class Motors

class Motors:

    def __init__(self, aStar):
        self.aStar = aStar
        self.trimL = 1
        self.trimR = 1. #.918 #.915
        self.dirL = 1 * self.trimL
        self.dirR = 1 * self.trimR
        self.maxFwdSpeed = 400
        self.maxRotSpeed = 300

    def speed(self, speedL, speedR):
        self.aStar.motors(speedL * self.dirL * self.maxFwdSpeed, speedR * self.dirR * self.maxFwdSpeed)

    def forward(self, speed):
        self.aStar.motors(speed * self.dirL * self.maxFwdSpeed, speed * self.dirR * self.maxFwdSpeed)
        
    def turn(self, rotSpeed):
        self.aStar.motors(-rotSpeed * self.dirL * self.maxRotSpeed, rotSpeed * self.dirR * self.maxRotSpeed)

    def stop(self):
        self.aStar.motors(0, 0)


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

    def __init__(self, analog, aPin, calObj):
        self.analog = analog[aPin]
        self.aPin = aPin
        self.type = 'IRAnalog'
        self.cal = calObj

    def setCal(self, calObj):
        self.cal = calObj

    def getObstDist(self):
        return self.cal.applyCal(self.analog)
##        if a > 40 and a < 900:
##            dist = -2.037E-12 * a**5 + 1.167E-8 * a**4 - 2.251E-5 * a**3 + 2.023E-2 * a**2 - 9.005 * a + 1.734E3

    def hasObst(self, distMin, distMax):
        obstDist = self.getObstDist()
        if obstDist != -1 and distMin <= obstDist and obstDist <= distMax:
            return True
        else:
            return False

class DDistSens:

    def __init__(self, analog, aPin):
        self.analog = analog[aPin]
        self.aPin = aPin
        self.type = 'IRDigital'

    def hasObst(self):
        if self.analog < 1023:
            return True
        else:
            return False

class Sensors: # Collection of sensors installed on the robot

    def __init__(self, aStar):
        self.aStar = aStar
        self.analog = aStar.read_analog()
        self.calIR = SensCalPoly('IR', 40, 900, 1.734E3, -9.005E0, 2.023E-2, -2.251E-5, 1.167E-8, -2.037E-12)
        self.irALeft = ADistSens(self.analog, 2, self.calIR)
        self.irARight = ADistSens(self.analog, 3, self.calIR)
        self.irDLeft = DDistSens(self.analog, 0)
        self.irDRight = DDistSens(self.analog, 4)

    def read(self):
        self.analog = self.aStar.read_analog()
        self.irALeft.analog = self.analog[self.irALeft.aPin]
        self.irARight.analog = self.analog[self.irARight.aPin]
        self.irDLeft.analog = self.analog[self.irDLeft.aPin]
        self.irDRight.analog = self.analog[self.irDRight.aPin]
        

# Class Encoders

# Class Robot

class Robot:

    def __init__(self):
        self.aStar = AStar()
        self.motors = Motors(self.aStar)
        self.sensors = Sensors(self.aStar)

    def readAStar(self):
        self.sensors.read()
        self.buttons = self.aStar.read_buttons()

    def forward(self, speed):
        self.motors.forward(speed)

    def turn(self, rotSpeed):
        self.motors.turn(rotSpeed)

    def move(self, speed, rotSpeed):
        self.motors.speed(speed - rotSpeed, speed + rotSpeed) 

    def stop(self):
        self.motors.stop()
