import threading
import time
from math import pi, sqrt
from Timer import Timer
from PID import PID


class MotionController:

    def __init__(self, odometer, motors, timeStep = .025):
        self.timeStep = timeStep
        self.odometer = odometer
        self.odometer.timeStep = self.timeStep
        self.motors = motors
        self.omegaPID = PID()
        self.targetV = 0
        self.targetOmega = 0
        self.mode = "STOPPED"
        self.move()
        
########################################################################
##  Movement control methods
########################################################################
        
    # Serial; Method will execute until the target distance is reached
    def forwardDist(self, speed, distTarget, stop = True, decel = True):
        phi0 = self.odometer.getPhi()
        x0, y0 = self.odometer.getPosXY()
        dist = 0
        loopTimer = Timer()
        if decel:
            while dist < distTarget - speed * 3 * self.timeStep:
                self.forwardAngle(speed, phi0)
                loopTimer.sleepToElapsed(self.timeStep)
                x1, y1 = self.odometer.getPosXY()
                dist = sqrt((x1 - x0)**2 + (y1 - y0)**2)
                if distTarget - dist < 50 and speed > 75:
                    speed = speed / 1.3
        else:
            while dist < distTarget:
                self.forwardAngle(speed, phi0)
                loopTimer.sleepToElapsed(self.timeStep)
                x1, y1 = self.odometer.getPosXY()
                dist = sqrt((x1 - x0)**2 + (y1 - y0)**2)
        if stop:
            self.stop()
        
    # In-loop; Need to call this method within a loop with a short time step
    # in order for the PID to adjust the turn rate (targetOmega).
    def forwardAngle(self, speed, angleTarget):
        self.setMode('FORWARD')
        self.odometer.update()
        self.targetSpeed = speed
        self.targetOmega = self.omegaPID.getOutput(0, -self.odometer.angleRelToPhi(angleTarget), self.timeStep)

    # Stops the movement
    def stop(self):
        self.targetV = 0
        self.targetOmega = 0

    # Serial; Method will execute until the target turn angle is achieved
    def turnAngle(self, angleTarget, omegaTarget = pi / 12):
        phi0 = self.odometer.getPhi()
        self.turnToAngle(phi0 + angleTarget, omegaTarget)

    # Serial; Method will execute until the target angle is reached
    def turnToAngle(self, angleTarget, omegaTarget = pi / 18):
        self.setMode('TURN')
        self.targetV = 0
        self.targetOmega = 0
        omegaMax = pi / 6.
        omegaMin = pi / 36.
        angleTol = pi/180.
        loopTimer = Timer()
        while abs(self.odometer.angleRelToPhi(angleTarget)) > angleTol:
            omega = self.omegaPID.getOutput(0, -self.odometer.angleRelToPhi(angleTarget), self.timeStep)
            if omega > omegaMax:
                omega = omegaMax
            elif omega < -omegaMax:
                omega = -omegaMax
            if omega > 0 and omega < omegaMin:
                omega = omegaMin
            elif omega < 0 and omega > -omegaMin:
                omega = -omegaMin
            self.targetOmega = omega
            loopTimer.sleepToElapsed(self.timeStep)
        self.stop()

########################################################################
##  Other methods
########################################################################

    # Kill thread running ._move() method
    def kill(self):
        self.active = False

    # This method runs continuously until self.active is set to false.
    # It looks for targetV and targetOmega values, provides corresponding
    # speed commands to the motors and updates the odometer at every pass
    # of the loop.
    def _move(self):
        loopTimer = Timer()
        while self.active:
            speedL = self.targetV - self.targetOmega * pi * self.odometer.track
            speedR = self.targetV + self.targetOmega * pi * self.odometer.track
            self.motors.speed(speedL, speedR)
            loopTimer.sleepToElapsed(self.timeStep)
            self.odometer.update()

    # Starts the ._move() method in a thread
    def move(self):
        self.active = True
        th = threading.Thread(target = self._move, args = [])
        th.start()

    # Sets the omegaPID constants for specific movement modes               
    def setMode(self, mode):
        if self.mode != mode:
            self.mode = mode
            self.omegaPID.reset()
            # Set PID constants for specific mode
            if mode == 'FORWARD':
                self.omegaPID.setKs(.41, 0, 0)
            if mode == 'TURN':
                self.omegaPID.setKs(1, 0, 0)

    def setTimeStep(self, timeStep):
        self.timeStep = timeStep
        self.odometer.timeStep = timeStep
