import math
import time
from Timer import Timer

# Function boundAngle(angle) takes any angle as "angle" and returns the equivalent angle bound within 0 <= angle < 2 * Pi
def boundAngle(angle):
    if angle < 0:
        angle = angle + 2 * math.pi
    if angle >= 2 * math.pi:
        angle = angle % (2 * math.pi)
    return angle

# Function relativeAngle(angleRef, angle) returns the shortest relative angle from a reference angle "angleRef"
# to an angle "angle". The retuned relative angle is bound within -Pi < angle < Pi
def relativeAngle(angleRef, angle):
    angleRef = boundAngle(angleRef)
    angle = boundAngle(angle)

    if angle - angleRef > math.pi:
        relativeAngle = angle - angleRef - 2 * math.pi
    elif angle - angleRef < -math.pi:
        relativeAngle = angle - angleRef + 2 * math.pi
    else:
        relativeAngle = angle - angleRef

    return relativeAngle
    

class Odometer:

    def __init__(self, encoders):
        self.encoders = encoders
        self.track = 146. # width between wheels in millimeters
##        self.distPerTick = 70 * math.pi / 720 # Wheel circumference / nb of ticks per revolution
        self.tick = .32938
        self.lastCountLeft = 0
        self.lastCountRight = 0
        self.phi = 0
        self.x = 0
        self.y = 0
        self.v = 0
        self.omega = 0
        self.timer = Timer()
        self.timeStep = 1
        self.active = False

    def update(self):
        self.timeStep = self.timer.getElapsed()
        self.timer.reset()
        countLeft, countRight = self.encoders.getCounts()

        deltaCountLeft = countLeft - self.lastCountLeft
        deltaCountRight = countRight - self.lastCountRight

        distLeft = deltaCountLeft * self.tick
        distRight = deltaCountRight * self.tick
        distCenter = (distLeft + distRight) / 2.
        
        self.x += distCenter * math.cos(self.phi)
        self.y += distCenter * math.sin(self.phi)

        deltaPhi = (distRight - distLeft) / self.track
        self.phi = boundAngle(self.phi + deltaPhi)
       
        if self.active:
            self.v = distCenter / self.timeStep
            self.omega = deltaPhi / self.timeStep
        else:
            self.active = True

        self.lastCountLeft = countLeft
        self.lastCountRight = countRight

    def getPosXY(self):
        return self.x, self.y

    def getPosXYPhi(self):
        return self.x, self.y, self.phi

    def getPhi(self):
        return self.phi

    def angleRelToPhi(self, angle):
        return relativeAngle(self.phi, angle)

    def getOmega(self):
        return self.omega

    def getSpeed(self):
        return self.v

    def resetEncoders(self):
        self.encoders.reset()
        self.lastCountLeft = 0
        self.lastCountRight = 0

    def resetPosXY(self):
        self.x = 0
        self.y = 0

    def resetPosXYPhi(self):
        self.phi = 0
        self.x = 0
        self.y = 0

    def resetTimer(self):
        self.timer.reset()
