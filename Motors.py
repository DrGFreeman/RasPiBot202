class Motors:

    def __init__(self, aStar):
        self.aStar = aStar
        self.trimL = 1
        self.trimR = 1
        self.dirL = 1 * self.trimL
        self.dirR = 1 * self.trimR
        self.maxFwdSpeed = 400
        self.maxRotSpeed = 300

    def speed(self, speedL, speedR):
        self.aStar.motors(speedL * self.dirL * self.maxFwdSpeed, speedR * self.dirR * self.maxFwdSpeed)

    def forward(self, speed):
        self.aStar.motors(speed * self.dirL * self.maxFwdSpeed, speed * self.dirR * self.maxFwdSpeed)
        
    def turn(self, rotSpeed):
        self.aStar.motors(-rotSpeed * self.dirL * self.maxRotSpeed, rotSpeed * self.dirR * self.maxRotSpeed)

    def stop(self):
        self.aStar.motors(0, 0)
