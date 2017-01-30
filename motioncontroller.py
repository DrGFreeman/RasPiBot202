import threading
import time
from math import pi, sqrt
from timer import Timer
from pid import PID


class MotionController:
    """A class that controls the robot movements via different serial or in-loop
    methods. It uses odometry information from the robot's odometer to set
    target speeds for the motors. Distances/positions and speeds are in mm and
    mm/s respectively and angles and turn rates are in radians and radians/s
    respectively (pi radians = 180 degrees). Angles and turn rates are positive
    in counterclockwise direction."""

    def __init__(self, odometer, motors, timeStep=.02):
        self.timeStep = timeStep
        self.odometer = odometer
        self.motors = motors
        self.omegaPID = PID()
        self.targetV = 0
        self.targetOmega = 0
        self.mode = "STOPPED"
        self.run()

########################################################################
##  Movement control methods
########################################################################

    def forwardDist(self, speed, distTarget, stop=True, decel=False):
        """Moves the robot forward a fixed distance (in mm). The robot will stop
        once the distance is reached unless stop is set to False. decel=True
        will have the robot slow down before stopping. Serial: this method will
        execute until the target distance is reached."""
        phi0 = self.odometer.getPhi()
        x0, y0 = self.odometer.getPosXY()
        speed0 = speed
        dist = 0
        loopTimer = Timer()
        if stop and decel:
            while dist < distTarget - .35 * speed:
                self.forwardAngle(speed, phi0)
                loopTimer.sleepToElapsed(self.timeStep)
                x1, y1 = self.odometer.getPosXY()
                dist = sqrt((x1 - x0)**2 + (y1 - y0)**2)
                if distTarget - dist < (.5 * speed0) and speed > 50:
                    speed = speed / 1.05
            self.stop()
        else:
            while dist < distTarget:
                self.forwardAngle(speed, phi0)
                loopTimer.sleepToElapsed(self.timeStep)
                x1, y1 = self.odometer.getPosXY()
                dist = sqrt((x1 - x0)**2 + (y1 - y0)**2)
            if stop:
                self.stop()

    def forwardAngle(self, speed, angleTarget):
        """Moves forward at a specified angle. A PID will ajust the turn rate
        omega to reach and maintain phi at angleTarget. In-loop: this method
        must be call from within a loop with a short time step for the PID to
        ajust the turn rate."""
        self.setMode('FORWARD')
        omega = self.omegaPID.getOutput(0,-self.odometer.angleRelToPhi(angleTarget),
                                        self.timeStep)
        self.setSpeed(speed, omega)

    def move(self, v, omega):
        """Same as setSpeed method. Kept for backward compatibility."""
        self.setSpeed(v, omega)

    def setSpeed(self, v, omega):
        """Sets the target forward and rotational speeds (v & omega). Forward
        speed v is in mm/s and the turn rate omega is in radians/s
        (180 degrees = pi radians)."""
        self.targetV = v
        self.targetOmega = omega

    def stop(self):
        """Stops the movement."""
        self.targetV = 0
        self.targetOmega = 0
        self.motors.stop()

    def turnAngle(self, angleTarget, omega = pi):
        """Turns a specified angle from current phi angle. angleTarget is in
        radians (pi radians = 180 degrees). The turn rate omega is in radians/s
        (default = pi = 180 deg/s). A positive angle corresponds to a
        counterclockwise rotation. If angleTarget is larger than pi (180 deg),
        the robot will take the shortest rotation direction to the target, i.e.
        will turn in the opposite direction. Serial: this method will execute
        until the target angle is reached."""
        phi0 = self.odometer.getPhi()
        self.turnToAngle(phi0 + angleTarget, omega)

    def turnToAngle(self, angleTarget, omega = pi):
        """Turns to a specified angle in the odometer absolute reference frame.
        The target angle is in radians (pi radians = 180 degrees). The turn rate
        omega is in radians/s (default = pi = 180 deg/s). The robot will take
        the shortest rotation direction to the target. Serial: this method will
        execute until the target angle is reached."""
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

    def kill(self):
        """Kills the thread running the _run method."""
        self.stop()
        self.active = False

    def _run(self):
        """This method runs continuously until self.active is set to false. It
        looks for targetV and targetOmega values, provides corresponding speed
        commands to the motors at every pass of the loop."""
        try:
            loopTimer = Timer()
            while self.active:
                speedL = self.targetV - self.targetOmega * self.odometer.track / 2.
                speedR = self.targetV + self.targetOmega * self.odometer.track / 2.
                self.motors.speed(speedL, speedR, self.timeStep)
                loopTimer.sleepToElapsed(self.timeStep)
        except IOError:
            print "IOError - Stopping"
            self.stop()
            self.kill()

    def run(self):
        """Starts the _run method in a thread."""
        self.active = True
        th = threading.Thread(target = self._run, args = [])
        th.start()

    def setMode(self, mode):
        """Sets the omegaPID constants for specific movement modes."""
        if self.mode != mode:
            self.mode = mode
            self.omegaPID.reset()
            # Set PID constants for specific mode
            if mode == 'FORWARD':
                self.omegaPID.setKs(1, 0, 0)
            if mode == 'TURN':
                self.omegaPID.setKs(1.5, 0, 0)
