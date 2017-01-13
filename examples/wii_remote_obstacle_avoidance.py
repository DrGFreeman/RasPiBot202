import sys
sys.path.append('../')
import numpy as np
from math import pi, degrees
import time

import robotbuilder
from timer import Timer
from wiiremote import WiiRemote

##  Build robot
rpb202 = robotbuilder.build()
rpb202.motionCtrl.setTimeStep(1/40.)

##  Define sensor parameters
sensAlphas = np.array([4*pi/16, pi/16, -pi/16, -4*pi/16])
sensMin = 60.
sensMax = 700.

##  Define constants
speedMax = 600.
omegaMax = 2 * pi
fps = 20

##  Define obstacle avoidance parameters
turnCorrRange = 400.
turnCorrGain = 4.

try:

    ##  Connect Wii remote
    wii = WiiRemote(1)
    wii.robotRemote(fps)
    time.sleep(.5)

    ##  Start loop timer
    lt = Timer()

    ##  Main loop
    end = False
    while not end:

        ##  Read Wii remote
        fwd = wii.stickV
        turn = -wii.stickH

        ##  Define stick deadzone
        zone = .05
        if -zone < fwd and fwd < zone:
            fwd = 0
        if -zone < turn and turn < zone:
            turn = 0

        ##  Define speed and turn rate
        speed = fwd * speedMax
        omega = turn * omegaMax

        ##  Read sensors
        rpb202.readAStar()
        readings = np.zeros(sensAlphas.size)
        for i in range(sensAlphas.size):
            if rpb202.sensors[i].hasObst(sensMin, sensMax):
                readings[i] = rpb202.sensors[i].getObstDist()
            else:
                readings[i] = sensMax

        ##  Calculate omega correction
        alphaCorr = (readings * sensAlphas).sum() / readings.sum()        
        omegaCorr = alphaCorr / readings.min() * speed
        #print readings, degrees(alphaCorr), degrees(omegaCorr)

        ##  Apply turn rate correction
        if readings.min() <= turnCorrRange and speed != 0:
            omega += turnCorrGain * omegaCorr

        ##  Adjust robot speed and turn rate
        rpb202.motionCtrl.setSpeed(speed, omega)

        ##  Wait till end of time step
        lt.sleepToElapsed(1./fps)
    


except KeyboardInterrupt:
    rpb202.stop()
    wii.release()
    rpb202.kill()
    print("KeyboardInterrupt")

finally:
    rpb202.stop()
    wii.release()
    rpb202.kill()
