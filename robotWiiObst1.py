import time
import robotBuilder
from WiiRemote import WiiRemote

##  Build Robot from robotBuilder (edit robotBuilder to customize robot)
rpb202 = robotBuilder.build()

##  Create direct pointers to robot sensors
irDL = rpb202.sensors[0]
irAL = rpb202.sensors[1]
snrCtr = rpb202.sensors[2]
irAR = rpb202.sensors[3]
irDR = rpb202.sensors[4]

try:

# WiiRemote - Constantes
    
    wii = WiiRemote(1)
    wii.robotRemote(20)
    time.sleep(.5)


    turnCorrRange = 450
    turnCorrGain = .2
    speedCorrRange = 200
    speedCorrGain = .7

    fwd = 0
    turn = 0

    tStep = .1

    end = False
    while not end:

        t0 = time.time()

        # Read aStar (sensors, buttons, etc.)
        rpb202.readAStar()

        # Set turn correction and speed correction off
        turnCorr = 0
        speedCorr = 1

        # Read sensors
        dL = irDL.hasObst()
        dR = irDR.hasObst()

        if irAL.hasObst(0, 600):
            aL = irAL.getObstDist()
            if aL < turnCorrRange:
                turnCorr += -turnCorrGain * (turnCorrRange - aL) / turnCorrRange
            if aL < speedCorrRange:
                speedCorr -= speedCorrGain * (speedCorrRange - aL) / speedCorrRange

        if irAR.hasObst(0, 600):
            aR = irAR.getObstDist()
            if aR < turnCorrRange:
                turnCorr += turnCorrGain * (turnCorrRange - aR) / turnCorrRange
            if aR < speedCorrRange:
                speedCorr -= speedCorrGain * (speedCorrRange - aR) / speedCorrRange

        print snrCtr.getObstDist()
##        if snrCtr.hasObst(0, 600):
##            aC = snrCtr.getObstDist()
##            if aC < speedCorrRange:
##                speedCorr -= speedCorrGain * (speedCorrRange - aC) / speedCorrRange
            

        if dL or dR:
            speedCorr = 0

##        print(dL, aL, aR, dR)
        
        
        fwd = wii.stickV
        turn = -wii.stickH

##        print fwd, turn

        if -.05 < fwd and fwd < .05:
            fwd = 0
        if -.05 < turn and turn < .05:
            turn = 0

        if wii.btnA:
            end = True

        fwd = fwd * speedCorr
        turn = turn + turnCorr

        if fwd < 0:
            turn = -turn

        rpb202.move(fwd, turn)

        dt = time.time() - t0
        if dt < tStep:
            time.sleep(tStep - dt)
        
    rpb202.stop()
    wii.release()

except KeyboardInterrupt:
    rpb202.stop()
    wii.release()
    print("KeyboardInterrupt")    
