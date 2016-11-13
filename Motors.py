from PID import PID
from Timer import Timer

class Motors:

    def __init__(self, aStar, encoders):
        self.aStar = aStar
        self.trimL = 1
        self.trimR = .95
        self.dirL = 1 * self.trimL
        self.dirR = 1 * self.trimR
        self.maxFwdCmd = 400
        self.maxRotCmd = 300
        self.prevCmdL = 0
        self.prevCmdR = 0
        self.accelStep = .07

        self.pidL = PID(.7, 6)
        self.pidR = PID(.7, 6)
        self.timer = Timer()
        self.tickDist = .32938 # Dist travelled per tick (in mm)
        self.speedCst = 742. # Approximate speed (in mm/s) for unit command
        self.lastCountL = 0
        self.lastCountR = 0
        self.speedL = 0
        self.speedR = 0

        self.timer.sleepToElapsed(.05)
        
        # Temporary fix to bypass defective pin B on left encoder
        self.encoders = encoders

    def speed(self, speedTargetL, speedTargetR):
        timeStep = self.timer.getElapsed()
        self.timer.reset()
        countL, countR = self.encoders.getCounts()

        deltaCountL = countL - self.lastCountL
        deltaCountR = countR - self.lastCountR

        self.speedL = deltaCountL * self.tickDist / timeStep
        self.speedR = deltaCountR * self.tickDist / timeStep
        cmdL = self.pidL.getOutput(speedTargetL, self.speedL, timeStep) / self.speedCst
        cmdR = self.pidR.getOutput(speedTargetR, self.speedR, timeStep) / self.speedCst

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
        
        self.aStar.motors(cmdL * self.dirL * self.maxFwdCmd, cmdR * self.dirR * self.maxFwdCmd)

        self.lastCountL += deltaCountL
        self.lastCountR += deltaCountR

    def cmd(self, cmdL, cmdR):
        # Limit motor acceleration
        if cmdL - self.prevCmdL > self.accelStep:
            cmdL = self.prevCmdL + self.accelStep
        if cmdR - self.prevCmdR > self.accelStep:
            cmdR = self.prevCmdR + self.accelStep
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
        self.aStar.motors(cmdL * self.dirL * self.maxFwdCmd, cmdR * self.dirR * self.maxFwdCmd)
        self.prevCmdL, self.prevCmdR = cmdL, cmdR

    def forward(self, cmd):
        self.aStar.motors(cmd * self.dirL * self.maxFwdCmd, cmd * self.dirR * self.maxFwdCmd)
        # Temporary fix to bypass defective pin B on left encoder
        self.setEncodersDir(cmd, cmd)
        
    def turn(self, rotCmd):
        self.aStar.motors(-rotCmd * self.dirL * self.maxRotCmd, rotCmd * self.dirR * self.maxRotCmd)

    def reset(self):
        self.pidL.reset()
        self.pidR.reset()
        self.lastCountL = 0
        self.lastCountR = 0
        self.speedL = 0
        self.speed = 0

    def stop(self):
        self.aStar.motors(0, 0)
        self.prevCmdL = 0
        self.prevCmdR = 0
        self.reset()

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
        
        
