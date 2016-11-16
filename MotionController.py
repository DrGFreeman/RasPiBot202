import math
import threading
import time

from Timer import Timer
from PID import PID


class MotionController:

    def __init__(self, odometer, motors):
        self.odometer = odometer
        self.motors = motors
        self.speedPID = PID()
        self.phiPID = PID()
        self.timeStep = .025
        self.mode = "STOPPED"

    # Serial
    def forwardDist(self, speed, distTarget):
        self.odometer.update()
        phi0 = self.odometer.getPhi()
        x0, y0 = self.odometer.getPosXY()
        dist = 0
        loopTimer = Timer()
        while dist < distTarget:
            self.forwardAngle(speed, phi0)
            loopTimer.sleepToElapsed(self.timeStep)
            x1, y1 = self.odometer.getPosXY()
            dist = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
            if distTarget - dist < 50 and speed > 75:
                speed = speed / 1.3
        self.stop()
        self.odometer.update()
        
    # In-loop
    def forwardAngle(self, speed, angle):
        self.setMode('FORWARD')
        self.odometer.update()
        turnSpeed = self.phiPID.getOutput(0, -self.odometer.angleRelToPhi(angle), self.odometer.timeStep)
        self.motors.speed(speed - turnSpeed, speed + turnSpeed)

    # Serial
    def turnAngle(self, angle):
        self.odometer.update()
        phi0 = self.odometer.getPhi()
        self.turnToAngle(phi0 + angle)

    # Serial
    def turnToAngle(self, angle):
        self.setMode('TURN')
        maxTurnCmd = .3
        minTurnCmd = .15 #.12
        turnPID = PID(.6) #.3
        timeStep = .05
        self.odometer.update()
        loopTimer = Timer()
        while abs(self.odometer.angleRelToPhi(angle)) > math.pi/180.:
            turnCmd = turnPID.getOutput(0, -self.odometer.angleRelToPhi(angle), timeStep)
            if turnCmd > maxTurnCmd:
                turnCmd = maxTurnCmd
            elif turnCmd < -maxTurnCmd:
                turnCmd = -maxTurnCmd
            if turnCmd > 0 and turnCmd < minTurnCmd:
                turnCmd = minTurnCmd
            elif turnCmd < 0 and turnCmd > -minTurnCmd:
                turnCmd = -minTurnCmd
            self.motors.cmd(-turnCmd, turnCmd)
            loopTimer.sleepToElapsed(timeStep)
            self.odometer.update()
        self.stop()
            
    def reset(self):
        self.speedPID.reset()
        self.phiPID.reset()
        self.odometer.resetTimer()
        self.odometer.resetEncoders()
        
    def setMode(self, mode):
        if self.mode != mode:
            self.mode = mode
            self.reset()
            # Set PID constants for specific mode
            if mode == 'FORWARD':
                self.phiPID.setKs(180., 65., .5)
                

    def stop(self):
        self.motors.stop()
        self.setMode('STOPPED')
