import math
import threading
import time

from Timer import Timer
from PID import PID


class MotionController:

    def __init__(self, odometer, motors, timeStep = .05):
        self.timeStep = timeStep
        self.odometer = odometer
        self.odometer.timeStep = self.timeStep
        self.motors = motors
        self.motors.timeStep = self.timeStep
        self.omegaPID = PID()
        self.mode = "STOPPED"
        

    # Serial; Method will execute until the target distance is reached
    def forwardDist(self, speed, distTarget):
        self.odometer.update()
        phi0 = self.odometer.getPhi()
        x0, y0 = self.odometer.getPosXY()
        dist = 0
        loopTimer = Timer()
        while dist < distTarget - speed * 3 * self.timeStep:
            self.forwardAngle(speed, phi0)
            loopTimer.sleepToElapsed(self.timeStep)
            x1, y1 = self.odometer.getPosXY()
            dist = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
            if distTarget - dist < 50 and speed > 75:
                speed = speed / 1.3
        self.stop()
        self.odometer.update()
        
    # In-loop; Need to call this method within a loop with a short time step
    # in order for the odometer to update and the PID to adjust the angle.
    def forwardAngle(self, speed, angleTarget):
        self.setMode('FORWARD')
        self.odometer.update()
        omega = self.omegaPID.getOutput(0, -self.odometer.angleRelToPhi(angleTarget), self.timeStep)
        speedL = speed - omega * math.pi * self.odometer.track
        speedR = speed + omega * math.pi * self.odometer.track
        self.motors.speed(speedL, speedR)

    # In-loop; Need to call this method within a loop with a short time step
    # in order for the odometer to update and the PID to adjust the angle.
    def move(self, speed, omega):
        self.setMode('MOVE')
        self.odometer.update()
        speedL = speed - omega * math.pi * self.odometer.track
        speedR = speed + omega * math.pi * self.odometer.track
        self.motors.speed(speedL, speedR)

    # Serial; Method will execute until the target turn angle is achieved
    def turnAngle(self, angleTarget, omegaTarget = math.pi / 12):
        self.odometer.update()
        phi0 = self.odometer.getPhi()
        self.turnToAngle(phi0 + angleTarget, omegaTarget)

    # Serial; Method will execute until the target angle is reached
    def turnToAngle(self, angleTarget, omegaTarget = math.pi / 18):
        self.setMode('TURN')
        omegaMax = math.pi / 6.
        omegaMin = math.pi / 36.
        self.odometer.update()
        loopTimer = Timer()
        while abs(self.odometer.angleRelToPhi(angleTarget)) > math.pi/180.:
            omega = self.omegaPID.getOutput(0, -self.odometer.angleRelToPhi(angleTarget), self.timeStep)
            if omega > omegaMax:
                omega = omegaMax
            elif omega < -omegaMax:
                omega = -omegaMax
            if omega > 0 and omega < omegaMin:
                omega = omegaMin
            elif omega < 0 and omega > -omegaMin:
                omega = -omegaMin
            speedL = -omega * math.pi * self.odometer.track
            speedR = omega * math.pi * self.odometer.track
            self.motors.speed(speedL, speedR)
            loopTimer.sleepToElapsed(self.timeStep)
            self.odometer.update()
        self.stop()
            
    def reset(self):
        self.omegaPID.reset()
        self.odometer.resetEncoders()
        
    def setMode(self, mode):
        if self.mode != mode:
            self.mode = mode
            self.reset()
            # Set PID constants for specific mode
            if mode == 'FORWARD':
                self.omegaPID.setKs(.41, 0, 0)
            if mode == 'TURN':
                self.omegaPID.setKs(1, 0, 0)

    def setTimeStep(self, timeStep):
        self.timeStep = timeStep
        self.odometer.timeStep = timeStep
        self.motors.timeStep = timeStep

    def stop(self):
        self.motors.stop()
        self.setMode('STOPPED')
