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
        self.mode = "STOPPED"

    def forward(self, speedCmd, distTarget):
        phi0 = self.odometer.getPhi()
        x0, y0 = self.odometer.getPosXY()
        dist = 0
        timeStep = .05
        loopTimer = Timer()
        while dist < distTarget:
            self.forwardAngle(speedCmd, phi0)
            loopTimer.sleepToElapsed(timeStep)
            self.odometer.update()
            x1, y1 = self.odometer.getPosXY()
            dist = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
##            if distTarget - dist < 100:
##                speedCmd = speedCmd / 1.2
##                print speedCmd
            print dist
        self.stop()
        

    def forwardAngle(self, speedCmd, angle):
        self.setMode('FORWARD')
        self.odometer.update()
        turnCmd = self.phiPID.getOutput(0, -self.odometer.angleRelToPhi(angle), self.odometer.timeStep)
        self.motors.cmd(speedCmd - turnCmd, speedCmd + turnCmd)

    def turnAngle(self, angle):
        self.odometer.update()
        phi0 = self.odometer.getPhi()
        self.turnToAngle(phi0 + angle)

    def turnToAngle(self, angle):
        self.setMode('TURN')
        maxTurnCmd = .3
        minTurnCmd = .15 #.12
        turnPID = PID(.6) #.3
        self.odometer.update()
        timeStep = .05
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
                self.phiPID.setKs(.25, .5)
##                self.speedPID.setKs(.01, .01)
                

    def stop(self):
        self.motors.stop()
        self.setMode('STOPPED')
