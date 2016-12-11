from math import pi, degrees
import time
import robotBuilder
from Timer import Timer

def report():
        print r.odometer.getPosXY(), r.odometer.lastCountLeft, r.odometer.lastCountRight

r = robotBuilder.build()

timer = Timer()
loopTimer = Timer()

try:

    r.motionCtrl.forwardDist(-100, 200)
    r.motionCtrl.setSpeed(200, pi/5)
    time.sleep(3)
    r.motionCtrl.forwardDist(200, 200, stop = False, decel = False)
    r.motionCtrl.forwardDist(200, 100, stop = True, decel = False)
    timer.reset()
    loopTimer.reset()
    while timer.isWithin(5):
        r.motionCtrl.forwardAngle(200, 2 * pi / 5)
        loopTimer.sleepToElapsed(.05)
    r.motionCtrl.turnToAngle(pi)
    r.motionCtrl.turnAngle(pi/2)
    print degrees(r.odometer.getPhi() - pi/2)

##    r.motionCtrl.forwardDist(250, 200, stop=False)
##    report()
##    r.motionCtrl.forwardDist(250, 40, stop=False)
##    report()
##    r.motionCtrl.forwardDist(150, 200)
##    report()
##    time.sleep(.5)

##    angle = pi/2
##
##    for i in range(8):
##        r.motionCtrl.turnToAngle((i + 1) * angle)
##        time.sleep(.1)
##        if i == 3:
##            angle = -angle
##        report()

    r.motionCtrl.stop()

except KeyboardInterrupt:
    r.motionCtrl.stop()
