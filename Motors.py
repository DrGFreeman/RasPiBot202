class Motors:

    def __init__(self, aStar, encoders):
        self.aStar = aStar
        self.trimL = 1
        self.trimR = 1
        self.dirL = 1 * self.trimL
        self.dirR = 1 * self.trimR
        self.maxFwdCmd = 400
        self.maxRotCmd = 300
        self.prevCmdL = 0
        self.prevCmdR = 0
        self.accelStep = .1
        # Temporary fix to bypass defective pin B on left encoder
        self.encoders = encoders

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
        if cmdR > 1:
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

    def stop(self):
        self.aStar.motors(0, 0)
        self.prevCmdL = 0
        self.prevCmdR = 0

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
        
        
