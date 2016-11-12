class Motors:

    def __init__(self, aStar, encoders):
        self.aStar = aStar
        self.trimL = 1
        self.trimR = 1
        self.dirL = 1 * self.trimL
        self.dirR = 1 * self.trimR
        self.maxFwdSpeed = 400
        self.maxRotSpeed = 300
        # Temporary fix to bypass defective pin B on left encoder
        self.encoders = encoders

    def speed(self, speedL, speedR):
        if speedL < -1:
            speedL = -1
        elif speedL > 1:
            speedL = 1
        if speedR < -1:
            speedR = -1
        if speedR > 1:
            speedR = 1
        self.aStar.motors(speedL * self.dirL * self.maxFwdSpeed, speedR * self.dirR * self.maxFwdSpeed)
        # Temporary fix to bypass defective pin B on left encoder
        self.setEncodersDir(speedL, speedR)

    def forward(self, speed):
        self.aStar.motors(speed * self.dirL * self.maxFwdSpeed, speed * self.dirR * self.maxFwdSpeed)
        # Temporary fix to bypass defective pin B on left encoder
        self.setEncodersDir(speed, speed)
        
    def turn(self, rotSpeed):
        self.aStar.motors(-rotSpeed * self.dirL * self.maxRotSpeed, rotSpeed * self.dirR * self.maxRotSpeed)

    def stop(self):
        self.aStar.motors(0, 0)

    # Temporary fix to bypass defective pin B on left encoder
    def setEncodersDir(self, speedL, speedR):
        if speedL >= 0:
            self.encoders.countSignLeft = 1
        else:
            self.encoders.countSignLeft = -1
        if speedR >= 0:
            self.encoders.countSignRight = 1
        else:
            self.encoders.countSignRight = -1
        
        
