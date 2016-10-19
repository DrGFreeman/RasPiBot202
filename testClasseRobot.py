import time

from Robot import Robot
from WiiRemote import WiiRemote


fwdSpeed = .6
rotSpeed = .3
oneTurn = 1.543 * .5 / rotSpeed


rpb202 = Robot()
irAL = rpb202.sensors.irALeft
irAR = rpb202.sensors.irARight
irDL = rpb202.sensors.irDLeft
irDR = rpb202.sensors.irDRight

try:
##    rpb202.forward(fwdSpeed)
##    sleep(3)
##    rpb202.turn(rotSpeed)
##    sleep(oneTurn / 2)
##    rpb202.forward(fwdSpeed)
##    sleep(3)

# WiiRemote - Constantes

    wiiHRange = 222 - 22
    wiiHCentre = 122
    wiiVRange = 231 - 38
    wiiVCentre = 134
    
    wii = WiiRemote(1)
    wii.robotRemote(60)
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
        if irAL.hasObst(600):
            aL = irAL.getObstDist()
            if aL < turnCorrRange:
                turnCorr += -turnCorrGain * (turnCorrRange - aL) / turnCorrRange
            if aL < speedCorrRange:
                speedCorr -= -speedCorrGain * (speedCorrRange - aL) / speedCorrRange
        else:
            aL = False
        if irAR.hasObst(600):
            aR = irAR.getObstDist()
            if aR < turnCorrRange:
                turnCorr += turnCorrGain * (turnCorrRange - aR) / turnCorrRange
            if aL < speedCorrRange:
                speedCorr -= -speedCorrGain * (speedCorrRange - aL) / speedCorrRange
        else:
            aR = False

        if dL or dR:
            speedCorr = 0

##        print(dL, aL, aR, dR)
        
        
        fwd = 1 * (float(wii.stickV) - wiiVCentre) / wiiVRange
        turn = 1 * (wiiHCentre - float(wii.stickH)) / wiiHRange

        if -.05 < fwd and fwd < .05:
            fwd = 0
        if -.05 < turn and turn < .05:
            turn = 0

        if wii.btnA:
            end = True

        fwd = fwd * speedCorr
        turn = turn + turnCorr

##        print fwd, turn

        
        rpb202.motors.speed(fwd - turn, fwd + turn)

        dt = time.time() - t0
        if dt < tStep:
            time.sleep(tStep - dt)
        
    rpb202.stop()
    wii.release()

except KeyboardInterrupt:
    rpb202.stop()
    wii.release()
    print("KeyboardInterrupt")
