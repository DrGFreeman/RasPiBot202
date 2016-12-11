import Robot
import Timer
import time
from math import pi

r = Robot.Robot()
r.motionCtrl.setTimeStep(.05)
time.sleep(.5)

r.motionCtrl.turnAngle(pi)

timer = Timer.Timer()
while timer.isWithin(2):
    r.motionCtrl.move(250, 0)
    time.sleep(.05)
r.motionCtrl.stop()
##
##
##timer.reset()
##while timer.isWithin(2):
##    r.motionCtrl.move(250, 0)
##    time.sleep(.05)
##r.motionCtrl.stop()

r.motionCtrl.forwardDist(250, 500, decel=False)
r.motionCtrl.forwardDist(250, 500)
