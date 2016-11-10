import math
import time

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
    elif Angle - AngleRef < math.pi:
        relativeAngle = angle - angleRef + 2 * math.pi

    return relativeAngle
    

class Odometer:

    def __init__(self, encoders):
        self.encoders = encoders
        self.track = 145 # width between wheels in millimeters
        self.distPerTick = 70 * math.pi / 720 # Wheel circumference / nb of ticks per revolution
        self.lastCountLeft = 0
        self.lastCountRight = 0
        self.phi = 0
        self.x = 0
        self.y = 0
        self.v = 0
        self.omega = 0
        self.lastUpdateTime = 0
        self.active = False

    def update(self):
        updateTime = time.time()
        
        countLeft, countRight = self.encoders.getCounts()

        deltaCountLeft = countLeft - self.lastCountLeft
        deltaCountRight = countRight - self.lastCountRight

        distLeft = deltaCountLeft * self.distPerTick
        distRight = deltaCountRight * self.distPerTick
        distCenter = (distLeft + distRight) / 2
        

        self.x += distCenter * math.cos(self.phi)
        self.y += distCenter * math.sin(self.phi)

        deltaPhi = (distRight - distLeft) / self.track
        self.phi = boundAngle(self.phi + deltaPhi)

        
        if self.active:
            timeStep = updateTime - self.lastUpdateTime
            self.v = distCenter / timeStep
            self.omega = deltaPhi / timeStep
        else:
            self.active = True

        self.lastCountLeft = countLeft
        self.lastCountRight = countRight
        self.lastUpdateTime = updateTime

    def getPosXY(self):
        return self.x, self.y

    def getPosXYPhi(self):
        return self.x, self.y, self.phi

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
