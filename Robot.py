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

class Sensors:

    def __init__(self, aStar):
        self.aStar = aStar
        self.analog = aStar.read_analog()
        self.irALeft = ADistSens(self.analog, 2, 1)
        self.irARight = ADistSens(self.analog, 3, 1)
        self.irDLeft = DDistSens(self.analog, 0)
        self.irDRight = DDistSens(self.analog, 4)

    def read(self):
        self.analog = self.aStar.read_analog()
        self.irALeft.analog = self.analog[self.irALeft.aPin]
        self.irARight.analog = self.analog[self.irARight.aPin]
        self.irDLeft.analog = self.analog[self.irDLeft.aPin]
        self.irDRight.analog = self.analog[self.irDRight.aPin]
        

class ADistSens:

    def __init__(self, analog, aPin, cal):
        self.analog = analog[aPin]
        self.aPin = aPin
        self.type = 'IRAnalog'
        self.cal = cal

    def getObstDist(self):
        a = self.analog
        if self.cal == 1:
            if a > 40 and a < 900:
                dist = -2.037E-12 * a**5 + 1.167E-8 * a**4 - 2.251E-5 * a**3 + 2.023E-2 * a**2 - 9.005 * a + 1.734E3
            else:
                dist = -1
        return dist

    def hasObst(self, distMax):
        obstDist = self.getObstDist()
        if obstDist != -1 and obstDist <= distMax:
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
        

# Class Encoders

# Class Robot

class Robot:

    def __init__(self):
        self.aStar = AStar()
        self.motors = Motors(self.aStar)
        self.sensors = Sensors(self.aStar)
##        self.irALeft = aDistSens(self.analog, 2, 1)
##        self.irARight = aDistSens(self.analog, 3, 1)
##        self.irDLeft = dDistSens(self.analog, 0)
##        self.irDRight = dDistSens(self.analog, 4)

    def readAStar(self):
        self.sensors.read()
        self.buttons = self.aStar.read_buttons()

    def forward(self, speed):
        self.motors.forward(speed)

    def turn(self, rotSpeed):
        self.motors.turn(rotSpeed)

    def stop(self):
        self.motors.stop()
