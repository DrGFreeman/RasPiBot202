from pid import PID
from encoders import Encoders

class Motors:

    def __init__(self, aStar, encoders, odometer):
        self.aStar = aStar
        self.odometer = odometer
        self.encoders = encoders
        self.trimL = 1
        self.trimR = .95
        self.dirL = 1 * self.trimL
        self.dirR = 1 * self.trimR
        self.maxCmd = 400
        self.pidL = PID(.7, 6)
        self.pidR = PID(.7, 6)
        self.speedCst = 742. # Approximate speed (in mm/s) for unit command

        
    # In-loop; This method is designed to be called within a loop with a short time step
    # Odometer.update() needs to be called in the loop to read the encoders counts. To
    # use this method independent from the odometer, change self.encoder.getCounts()
    # for self.encoders.readCounts() on the first line of the method.
    # speedTarget arguments are in mm/s.
    def speed(self, speedTargetL, speedTargetR):

        speedL, speedR = self.odometer.getSpeedLR()

        cmdL = self.pidL.getOutput(speedTargetL, speedL, self.odometer.timeStep) / self.speedCst
        cmdR = self.pidR.getOutput(speedTargetR, speedR, self.odometer.timeStep) / self.speedCst

        # Limit motor command
        if cmdL < -1:
            cmdL = -1
        elif cmdL > 1:
            cmdL = 1
        if cmdR < -1:
            cmdR = -1
        elif cmdR > 1:
            cmdR = 1

        # Ensure faster stop
        if speedTargetL == 0 and speedTargetR == 0:
            cmdL, cmdR = 0, 0
        
        # Temporary fix to bypass defective pin B on left encoder
        self.setEncodersDir(cmdL, cmdR)
        
        self.aStar.motors(cmdL * self.dirL * self.maxCmd, cmdR * self.dirR * self.maxCmd)


    # In-loop; This method is to be called from within a loop.
    # cmd arguments are the motor speed commands ranging from -1 to 1 (-max to max speed)
    def cmd(self, cmdL, cmdR):
        # Limit motor command
        if cmdL < -1:
            cmdL = -1
        elif cmdL > 1:
            cmdL = 1
        if cmdR < -1:
            cmdR = -1
        elif cmdR > 1:
            cmdR = 1
        # Temporary fix to bypass defective pin B on left encoder
        self.setEncodersDir(cmdL, cmdR)
        # Command motors
        self.aStar.motors(cmdL * self.dirL * self.maxCmd, cmdR * self.dirR * self.maxCmd)

    def forward(self, cmd):
        self.aStar.motors(cmd * self.dirL * self.maxCmd, cmd * self.dirR * self.maxCmd)
        # Temporary fix to bypass defective pin B on left encoder
        self.setEncodersDir(cmd, cmd)
        
    def turn(self, rotCmd):
        self.aStar.motors(-rotCmd * self.dirL * self.maxCmd, rotCmd * self.dirR * self.maxCmd)

    def reset(self):
        self.pidL.reset()
        self.pidR.reset()

    def stop(self):
        self.aStar.motors(0, 0)

    # Temporary fix to bypass defective pin B on left encoder
    def setEncodersDir(self, cmdL, cmdR):
        if cmdL >= 0:
            self.encoders.countSignLeft = 1
        else:
            self.encoders.countSignLeft = -1
        if cmdR >= 0:
            self.encoders.countSignRight = 1
        else:
            self.encoders.countSignRight = -1
        
        
