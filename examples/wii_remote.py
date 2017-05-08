import sys
sys.path.append('../')
import time
import math

import robotbuilder
from timer import Timer
from wiiremote import WiiRemote

def goToPoint((xTarget, yTarget), speed = 225):
        x, y = rpb202.odometer.getPosXY()
        dist = math.sqrt((x - xTarget)**2 + (y - yTarget)**2)
        angle = math.atan2(yTarget - y, xTarget - x)
        rpb202.motionCtrl.turnToAngle(angle)
        while dist > 50:
            rpb202.motionCtrl.forwardAngle(speed, angle)
            time.sleep(.05)
            x, y = rpb202.odometer.getPosXY()
            dist = math.sqrt((x - xTarget)**2 + (y - yTarget)**2)
            angle = math.atan2(yTarget - y, xTarget - x)
        rpb202.motionCtrl.forwardDist(speed, 50, stop=True, decel=True)

##  Build robot
rpb202 = robotbuilder.build()
rpb202.motionCtrl.setTimeStep(1/40.)

##  Define constants
speedMax = 450.
omegaMax = 5.
fps = 20

##  Define empty path
path = []

btnZPrevState = False

try:

    ##  Connect Wii remote
    wii = WiiRemote(1)
    wii.robotRemote(fps)
    time.sleep(.5)

    step = 0

    ##  Start loop timer
    lt = Timer()

    ##  Main loop
    end = False
    while not end:

        ## Print position
        if step % 10 == 0:
            print rpb202.odometer.getPosXYPhi()

        ##  Read Wii remote
        fwd = wii.stickV * 2
        turn = -wii.stickH * 2

        ##  Define stick deadzone
        zone = .08
        if -zone < fwd and fwd < zone:
            fwd = 0
        if -zone < turn and turn < zone:
            turn = 0

        ##  Define speed and turn rate
        speed = fwd * speedMax
        omega = turn * omegaMax

        ##  Adjust robot speed and turn rate
        rpb202.motionCtrl.setSpeed(speed, omega)

        ## End if button A is pressed
        if wii.btnA:
            end = True

        ## Mark waypoint if button Z is pressed
        if wii.btnZ and not btnZPrevState:
            path.append(rpb202.odometer.getPosXY())
            print "Point marked as waypoint", path[-1]
            print path
        btnZPrevState = wii.btnZ
        
        ##  Wait till end of time step
        lt.sleepToElapsed(1./fps)

        step += 1

    ## Go back to origin following path
    path.reverse()
    for point in path:
        goToPoint(point)
    

    rpb202.stop()
    rpb202.motionCtrl.turnToAngle(0)
    print rpb202.odometer.getPosXYPhi()

except KeyboardInterrupt:
    print("KeyboardInterrupt")

finally:
    rpb202.stop()
    wii.release()
    rpb202.kill()
