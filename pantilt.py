from Servo import Servo

class PanTilt:

    def __init__(self, panPin, tiltPin):
        self.panPin = panPin
        self.tiltPin = tiltPin
        self.pan = Servo(self.panPin)
        self.tilt = Servo(self.tiltPin)

    def setPanTilt(self, pan, tilt):
        self.pan.move(pan)
        self.tilt.move(tilt)

    def sweep(self):
        self.pan.sweep()
        self.tilt.sweep()

    def center(self):
        self.pan.center()
        self.tilt.center()



