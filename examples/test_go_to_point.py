##  Test "Go-To Point" function to be implemented in a future "Navigator" class

##  Import libraries
import sys
sys.path.append('../')
import robotbuilder

##  Specific libraries to be imported in class:
import numpy as np
from math import atan2, pi, sqrt
from timer import Timer

##  Create Robot object instance
rpb202 = robotbuilder.build()

tStep = .02

def goToPoint(point, speed):
    lt = Timer()
    angle, dist = angleDistToPoint(point)
    #print angle, dist
    rpb202.motionCtrl.turnToAngle(angle)
    while dist > 100:
        rpb202.motionCtrl.forwardAngle(speed, angle)
        lt.sleepToElapsed(.02)
        angle, dist = angleDistToPoint(point)
    rpb202.motionCtrl.forwardDist(speed, dist, decel=True)
    rpb202.stop()
    print rpb202.odometer.getPosXY()

def angleDistToPoint(point):
    position = np.array(rpb202.odometer.getPosXY())
    dx, dy = point - position
    angle = atan2(dy, dx) % (2 * pi)
    dist = sqrt(dx**2 + dy**2)
    return angle, dist

try:

    points = [(1000, 400), (1800, -800), (2400, 500), (0, 0)]
    for point in points:
        print "Point suivant:", point
        goToPoint(point, 200)
    print rpb202.odometer.getPosXY()
    print rpb202.odometer.dist
    
    
    
except KeyboardInterrupt:
    print "Keyboard Interrupt"
    rpb202.stop()
    rpb202.kill()

finally:
    rpb202.stop()
    rpb202.kill()
