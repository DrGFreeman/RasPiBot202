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

    def forwardAngle(self, speedCmd, angle):
        self.setMode('FORWARD')
        self.odometer.update()
        turnCmd = self.phiPID.getOutput(0, -self.odometer.angleRelToPhi(angle), self.odometer.timeStep)
##        turnCmd = self.omegaPID.getOutput(0., self.odometer.getOmega(), self.odometer.timeStep)
##        speedCmd = self.speedPID.getOutput(speed, self.odometer.getSpeed(), self.odometer.timeStep)
        self.motors.cmd(speedCmd - turnCmd, speedCmd + turnCmd)

    def turnAngle(self, angle):
        self.setMode('TURN')
        timeStep = .05
        maxTurnCmd = .3
        minTurnCmd = .12
        turnPID = PID(.3)
        self.odometer.update()
        loopTimer = Timer()
        while abs(self.odometer.angleRelToPhi(angle)) > math.pi/180.:
##            print self.odometer.angleRelToPhi(angle)
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
