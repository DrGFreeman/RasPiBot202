from servo import Servo

class PanTilt:

    def __init__(self, panPin, tiltPin):
        self.panPin = panPin
        self.tiltPin = tiltPin
        self.pan = Servo(self.panPin, pwMin=.0008,
                         pwCtr=.00157, pwMax=.0022, dir=1)
        self.tilt = Servo(self.tiltPin, pwMin=.0008,
                          pwCtr=.00143, pwMax=.00207, dir=-1)

    def center(self):
        self.pan.center()
        self.tilt.center()

    def down(self):
        self.setPanTilt(0, -1)
        
    def setPanTilt(self, pan, tilt):
        self.pan.move(pan)
        self.tilt.move(tilt)

    def sweep(self):
        self.pan.sweep()
        self.tilt.sweep()




