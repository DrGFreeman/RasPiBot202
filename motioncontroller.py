import threading
import time
from math import pi, sqrt
from timer import Timer
from pid import PID


class MotionController:

    def __init__(self, odometer, motors, timeStep = .01):
        self.timeStep = timeStep
        self.odometer = odometer
        self.odometer.timeStep = self.timeStep
        self.motors = motors
        self.omegaPID = PID()
        self.targetV = 0
        self.targetOmega = 0
        self.mode = "STOPPED"
        self.run()
        
########################################################################
##  Movement control methods
########################################################################
        
    # Serial; Method will execute until the target distance is reached
    def forwardDist(self, speed, distTarget, stop = True, decel = False):
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
        omega = self.omegaPID.getOutput(0, -self.odometer.angleRelToPhi(angleTarget), self.timeStep)
        self.setSpeed(speed, omega)

    # Same as setSpeed method. Kept for backward compatibility
    def move(self, v, omega):
        self.setSpeed(v, omega)
        
    # Sets the target forward & rotational speeds (v & omega)
    def setSpeed(self, v, omega):
        self.targetV = v
        self.targetOmega = omega

    # Stops the movement
    def stop(self):
        self.targetV = 0
        self.targetOmega = 0
        self.motors.stop()

    # Serial; Method will execute until the target turn angle is achieved
    def turnAngle(self, angleTarget, omega = pi):
        phi0 = self.odometer.getPhi()
        self.turnToAngle(phi0 + angleTarget, omega)

    # Serial; Method will execute until the target angle is reached
    def turnToAngle(self, angleTarget, omega = pi):
        self.setMode('TURN')
        self.targetV = 0
        self.targetOmega = 0
        omegaMin = pi / 8.
        angleTol = pi/180.
        loopTimer = Timer()
        while abs(self.odometer.angleRelToPhi(angleTarget)) > angleTol:
            angle = self.odometer.angleRelToPhi(angleTarget)
            if angle > pi / 6:
                self.targetOmega = omega
            elif angle > 0:
                self.targetOmega = omegaMin
            elif angle < -pi / 6:
                self.targetOmega = -omega
            else:
                self.targetOmega = -omegaMin
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
    def _run(self):
        try:
            loopTimer = Timer()
            while self.active:
                speedL = self.targetV - self.targetOmega * self.odometer.track / 2.
                speedR = self.targetV + self.targetOmega * self.odometer.track / 2.
                self.motors.speed(speedL, speedR)
                loopTimer.sleepToElapsed(self.timeStep)
                self.odometer.update()
        except IOError:
            print "IOError - Stopping"
            self.stop()
            self.kill()

    # Starts the ._run() method in a thread
    def run(self):
        self.active = True
        th = threading.Thread(target = self._run, args = [])
        th.start()

    # Sets the omegaPID constants for specific movement modes               
    def setMode(self, mode):
        if self.mode != mode:
            self.mode = mode
            self.omegaPID.reset()
            # Set PID constants for specific mode
            if mode == 'FORWARD':
                self.omegaPID.setKs(1, 0, 0)
            if mode == 'TURN':
                self.omegaPID.setKs(1.5, 0, 0)

    def setTimeStep(self, timeStep):
        self.timeStep = timeStep
        self.odometer.timeStep = timeStep
