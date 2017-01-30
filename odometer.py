import time
from math import pi, cos, sin
import numpy as np
from filters import Filter1D

def boundAngle(angle):
    """Function boundAngle(angle) takes any angle as "angle" and returns the
    equivalent angle bound within 0 <= angle < 2 * Pi."""
    return angle % (2 * pi)


def relativeAngle(angleRef, angle):
    """Function relativeAngle(angleRef, angle) returns the shortest relative
    angle from a reference angle "angleRef" to an angle "angle". The retuned
    relative angle is bound within -Pi < angle < Pi."""
    angleRef = boundAngle(angleRef)
    angle = boundAngle(angle)

    if angle - angleRef > pi:
        relativeAngle = angle - angleRef - 2 * pi
    elif angle - angleRef < -pi:
        relativeAngle = angle - angleRef + 2 * pi
    else:
        relativeAngle = angle - angleRef

    return relativeAngle


class Odometer:

    def __init__(self, encoders):
        self.encoders = encoders
        self.timeStep = .01
        self.track = 142.5 # width between wheels in millimeters
        self.tickDist = .152505 # Distance travelled for per encoder click in millimeters
        self.lastCountLeft = 0
        self.lastCountRight = 0
        self.lastUTime = time.time()
        self.speedL = Filter1D(5)
        self.speedR = Filter1D(5)
        self.speedL.addDataPoint(np.zeros(5))
        self.speedR.addDataPoint(np.zeros(5))
        self.phi = 0
        self.x = 0
        self.y = 0
        self.v = 0
        self.omega = 0
        self.dist = 0
        self.active = False

    def update(self, uTime):

        countLeft, countRight = self.encoders.getCounts()

        deltaCountLeft = countLeft - self.lastCountLeft
        deltaCountRight = countRight - self.lastCountRight

        distLeft = deltaCountLeft * self.tickDist
        distRight = deltaCountRight * self.tickDist
        distCenter = (distLeft + distRight) / 2.
        self.dist += distCenter

        self.x += distCenter * cos(self.phi)
        self.y += distCenter * sin(self.phi)

        deltaPhi = (distRight - distLeft) / self.track
        self.phi = boundAngle(self.phi + deltaPhi)

        self.timeStep = uTime - self.lastUTime

        self.speedL.addDataPoint(distLeft / self.timeStep)
        self.speedR.addDataPoint(distRight / self.timeStep)
        self.v = distCenter / self.timeStep
        self.omega = deltaPhi / self.timeStep

        self.lastCountLeft = countLeft
        self.lastCountRight = countRight
        self.lastUTime = uTime

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

    def getSpeedLR(self):
        return self.speedL.getMedian(), self.speedR.getMedian()

    def resetDist(self):
        self.dist = 0

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
