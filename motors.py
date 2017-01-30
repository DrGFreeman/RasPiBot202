from pid import PID

class Motors:

    def __init__(self, aStar, odometer):
        self.aStar = aStar
        self.odometer = odometer
        self.trimL = 1
        self.trimR = .78
        self.dirL = 1 * self.trimL
        self.dirR = 1 * self.trimR
        self.maxCmd = 400
        self.pidL = PID(.5, 6)
        self.pidR = PID(.5, 6)
        self.speedCst = 800. # Approximate speed (in mm/s) for unit command

    def speed(self, targetSpeedL, targetSpeedR, timeStep):
        """Sets the motors commands to achieve the target speeds using a PID
        controller for each motor. This method is called in a loop from the
        robot.motionCtrl._run() method with a short time step for the PID
        controllers to update their error terms."""

        ##  Get wheels speed from odometer
        speedL, speedR = self.odometer.getSpeedLR()

        ##  Get commands from PID controllers
        cmdL = self.pidL.getOutput(targetSpeedL, speedL, timeStep) \
                    / self.speedCst
        cmdR = self.pidR.getOutput(targetSpeedR, speedR, timeStep) \
                    / self.speedCst

        ##  Limit motor commands to unit value
        if cmdL < -1:
            cmdL = -1
        elif cmdL > 1:
            cmdL = 1
        if cmdR < -1:
            cmdR = -1
        elif cmdR > 1:
            cmdR = 1

        ##  Ensure fast stop
        if targetSpeedL == 0 and targetSpeedR == 0:
            cmdL, cmdR = 0, 0

        ##  Set motor commands
        self.aStar.motors(cmdL * self.dirL * self.maxCmd,
                          cmdR * self.dirR * self.maxCmd)

    def reset(self):
        """Resets the PID controllers."""
        self.pidL.reset()
        self.pidR.reset()

    def stop(self):
        """Stops the motors and resets the PID controllers."""
        self.aStar.motors(0, 0)
        self.reset()
