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

    def forwardAngle(self, speed, angle):
        self.setMode('FORWARD')
        self.odometer.update()
        turnCmd = self.phiPID.getOutput(angle, self.odometer.angleRelToPhi(angle), self.odometer.timeStep)
##        turnCmd = self.omegaPID.getOutput(0., self.odometer.getOmega(), self.odometer.timeStep)
##        speedCmd = self.speedPID.getOutput(speed, self.odometer.getSpeed(), self.odometer.timeStep)
        speedCmd = speed
        self.motors.speed(speedCmd - turnCmd, speedCmd + turnCmd)

    def turnAngle(self, turnSpeed, angle):
        self.setMode('TURN')
        self.odometer.update()
        loopTimer = Timer()
        while abs(self.odometer.angleRelToPhi(angle)) > .05:
            angleError = self.odometer.angleRelToPhi(angle)
            print self.odometer.getPhi()
            turnCmd = .5 * angleError
            if turnCmd > turnSpeed:
                turnCmd = turnSpeed
            elif turnCmd < -turnSpeed:
                turnCmd = -turnSpeed
            self.motors.speed(-turnCmd, turnCmd)
            loopTimer.sleepToElapsed(.05)
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
                self.phiPID.setKs(.4, .2)
##                self.speedPID.setKs(.01, .01)
                

    def stop(self):
        self.motors.stop()
        self.setMode('STOPPED')
